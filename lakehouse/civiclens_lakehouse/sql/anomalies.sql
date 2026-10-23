-- Anomaly detectors. Deterministic SQL; every flagged row carries its peer group, baseline, score and limits.
-- Parameters are substituted by the runner: {baseline_fys} (settled years), {min_peer_n}, {z_threshold},
-- {hhi_threshold}, {hhi_top_share}, {hhi_min_spend}, {growth_ratio}, {growth_min_delta}, {growth_min_base}.

-- 1. Unusually large award-year obligation within (agency, PSC 2-char class, FY); robust z on log10.
CREATE OR REPLACE TABLE anomaly_large_award AS
WITH pos AS (
  SELECT *, LOG10(obligations) AS lg FROM gold_award_fy WHERE obligations > 0
),
peer AS (
  SELECT awarding_agency_code, psc_class2, fiscal_year,
         COUNT(*) AS peer_n, MEDIAN(lg) AS med_lg
  FROM pos GROUP BY awarding_agency_code, psc_class2, fiscal_year
),
mad AS (
  SELECT p.awarding_agency_code, p.psc_class2, p.fiscal_year, MEDIAN(ABS(x.lg - p.med_lg)) AS mad_lg
  FROM pos x JOIN peer p USING (awarding_agency_code, psc_class2, fiscal_year)
  GROUP BY p.awarding_agency_code, p.psc_class2, p.fiscal_year
),
scored AS (
  SELECT x.*, p.peer_n, p.med_lg, m.mad_lg,
         CASE WHEN m.mad_lg > 0 THEN (x.lg - p.med_lg) / (1.4826 * m.mad_lg) END AS robust_z
  FROM pos x JOIN peer p USING (awarding_agency_code, psc_class2, fiscal_year)
             JOIN mad  m USING (awarding_agency_code, psc_class2, fiscal_year)
)
SELECT 'large_award' AS detector, award_key, piid, fiscal_year, awarding_agency_code, awarding_agency_name,
       recipient_uei, recipient_name, psc, psc_class2,
       obligations AS value, 'USD obligated in fiscal year' AS unit,
       peer_n, POWER(10, med_lg) AS baseline_median, mad_lg AS baseline_mad_log10, robust_z AS score, {z_threshold} AS threshold,
       CASE WHEN peer_n < {min_peer_n} THEN 'not scored: fewer than {min_peer_n} comparable award-years'
            WHEN mad_lg IS NULL OR mad_lg = 0 THEN 'not scored: no spread in peer group'
            WHEN robust_z >= {z_threshold} THEN 'flagged'
            ELSE 'normal' END AS status,
       'Peer group: awards from the same awarding agency, same 2-character PSC class, same fiscal year. ' ||
       'PSC classes group dissimilar services; a large value can be ordinary for a multi-year vehicle or a consolidated buy. ' ||
       'Statistically unusual relative to this comparison group; not a finding of wrongdoing.' AS limits,
       usaspending_permalink
FROM scored;

-- 2. Vendor concentration within (agency, PSC class, FY): Herfindahl-Hirschman index of recipient shares.
CREATE OR REPLACE TABLE anomaly_concentration AS
WITH cell AS (
  SELECT awarding_agency_code, MAX(awarding_agency_name) AS awarding_agency_name, psc_class2, fiscal_year, recipient_uei,
         MAX(recipient_name) AS recipient_name, SUM(obligations) AS obl
  FROM gold_award_fy WHERE obligations > 0 GROUP BY awarding_agency_code, psc_class2, fiscal_year, recipient_uei
),
tot AS (
  SELECT awarding_agency_code, psc_class2, fiscal_year, SUM(obl) AS total, COUNT(*) AS n_recipients FROM cell
  GROUP BY awarding_agency_code, psc_class2, fiscal_year
),
hhi AS (
  SELECT c.awarding_agency_code, MAX(c.awarding_agency_name) AS awarding_agency_name, c.psc_class2, c.fiscal_year,
         MAX(t.total) AS total, MAX(t.n_recipients) AS n_recipients,
         SUM(POWER(100.0 * c.obl / t.total, 2)) AS hhi,
         MAX(100.0 * c.obl / t.total) AS top_share
  FROM cell c JOIN tot t USING (awarding_agency_code, psc_class2, fiscal_year)
  GROUP BY c.awarding_agency_code, c.psc_class2, c.fiscal_year
),
top AS (
  SELECT c.awarding_agency_code, c.psc_class2, c.fiscal_year, c.recipient_uei AS top_recipient_uei, c.recipient_name AS top_recipient_name
  FROM cell c JOIN (SELECT awarding_agency_code, psc_class2, fiscal_year, MAX(obl) AS mx FROM cell GROUP BY 1,2,3) m
    ON c.awarding_agency_code = m.awarding_agency_code AND c.psc_class2 = m.psc_class2 AND c.fiscal_year = m.fiscal_year AND c.obl = m.mx
),
prior AS (
  SELECT awarding_agency_code, psc_class2, fiscal_year + 1 AS fiscal_year, hhi AS prior_hhi FROM hhi
)
SELECT 'concentration' AS detector, h.awarding_agency_code, h.awarding_agency_name, h.psc_class2, h.fiscal_year,
       h.total AS value, 'USD obligated in cell' AS unit, h.n_recipients AS peer_n, h.hhi AS score, {hhi_threshold} AS threshold,
       h.top_share, t.top_recipient_uei, t.top_recipient_name, p.prior_hhi, h.hhi - p.prior_hhi AS hhi_change,
       CASE WHEN h.total < {hhi_min_spend} THEN 'not scored: cell below spend floor'
            WHEN (h.hhi >= {hhi_threshold} AND h.top_share >= {hhi_top_share}) OR (p.prior_hhi IS NOT NULL AND h.hhi - p.prior_hhi >= 1000) THEN 'flagged'
            ELSE 'normal' END AS status,
       'HHI over recipient shares of obligations in one agency, PSC class and fiscal year (10,000 = one recipient). ' ||
       'Small cells and sole-source categories are concentrated by nature. Statistically unusual relative to this ' ||
       'comparison group; not a finding of wrongdoing.' AS limits
FROM hhi h LEFT JOIN top t USING (awarding_agency_code, psc_class2, fiscal_year)
           LEFT JOIN prior p USING (awarding_agency_code, psc_class2, fiscal_year);

-- 3. Abrupt recipient growth at one agency year over year.
CREATE OR REPLACE TABLE anomaly_recipient_growth AS
WITH cur AS (SELECT * FROM gold_recipient_agency_fy),
prev AS (SELECT recipient_uei, awarding_agency_code, fiscal_year + 1 AS fiscal_year, obligations AS prior_obligations FROM gold_recipient_agency_fy)
SELECT 'recipient_growth' AS detector, c.recipient_uei, c.recipient_name, c.awarding_agency_code, c.awarding_agency_name, c.fiscal_year,
       c.obligations AS value, 'USD obligated in fiscal year' AS unit, p.prior_obligations AS baseline,
       c.obligations - p.prior_obligations AS delta,
       CASE WHEN p.prior_obligations > 0 THEN c.obligations / p.prior_obligations END AS score, {growth_ratio} AS threshold,
       c.awards,
       CASE WHEN p.prior_obligations IS NULL THEN 'not scored: no prior-year obligations at this agency'
            WHEN p.prior_obligations < {growth_min_base} THEN 'not scored: prior year below base floor'
            WHEN c.obligations / p.prior_obligations >= {growth_ratio} AND c.obligations - p.prior_obligations >= {growth_min_delta} THEN 'flagged'
            ELSE 'normal' END AS status,
       'Ratio of this fiscal year''s obligations to the prior year for the same recipient at the same awarding agency. ' ||
       'New large vehicles and option-year exercises produce legitimate jumps. Statistically unusual relative to this ' ||
       'comparison; not a finding of wrongdoing.' AS limits
FROM cur c LEFT JOIN prev p USING (recipient_uei, awarding_agency_code, fiscal_year);
