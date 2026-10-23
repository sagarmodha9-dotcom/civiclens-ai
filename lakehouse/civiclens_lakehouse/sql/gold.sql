-- Gold: analytical grains. Every figure on the site comes from one of these tables, and every one of them
-- is a SUM over silver rows, so Gold reconciles to Silver to the cent by construction (tested).
CREATE OR REPLACE TABLE gold_award_fy AS
SELECT award_key, piid, parent_piid, fiscal_year,
       awarding_agency_code, MAX(awarding_agency_name) AS awarding_agency_name,
       MAX(awarding_sub_agency_name) AS awarding_sub_agency_name,
       recipient_uei, MAX(recipient_name) AS recipient_name,
       MAX(psc) AS psc, MAX(psc_class2) AS psc_class2, MAX(it_category) AS it_category, MAX(naics) AS naics,
       MAX(award_type_code) AS award_type_code,
       SUM(obligation) AS obligations, COUNT(*) AS transactions,
       SUM(CASE WHEN obligation < 0 THEN obligation ELSE 0 END) AS deobligations,
       MIN(action_date) AS first_action_date, MAX(action_date) AS last_action_date,
       MAX(usaspending_permalink) AS usaspending_permalink
FROM silver_contract_transactions
GROUP BY award_key, piid, parent_piid, fiscal_year, awarding_agency_code, recipient_uei;

CREATE OR REPLACE TABLE gold_agency_fy AS
SELECT awarding_agency_code, MAX(awarding_agency_name) AS awarding_agency_name, fiscal_year, it_category,
       SUM(obligation) AS obligations, COUNT(*) AS transactions, COUNT(DISTINCT award_key) AS awards,
       COUNT(DISTINCT recipient_uei) AS recipients
FROM silver_contract_transactions GROUP BY awarding_agency_code, fiscal_year, it_category;

CREATE OR REPLACE TABLE gold_recipient_agency_fy AS
SELECT recipient_uei, MAX(recipient_name) AS recipient_name, awarding_agency_code, MAX(awarding_agency_name) AS awarding_agency_name,
       fiscal_year, SUM(obligation) AS obligations, COUNT(DISTINCT award_key) AS awards, COUNT(*) AS transactions
FROM silver_contract_transactions GROUP BY recipient_uei, awarding_agency_code, fiscal_year;

CREATE OR REPLACE TABLE gold_psc_fy AS
SELECT awarding_agency_code, fiscal_year, psc_class2, MAX(psc_description) AS psc_example_description,
       SUM(obligation) AS obligations, COUNT(DISTINCT award_key) AS awards, COUNT(DISTINCT recipient_uei) AS recipients
FROM silver_contract_transactions GROUP BY awarding_agency_code, fiscal_year, psc_class2;
