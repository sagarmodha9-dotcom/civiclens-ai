-- Silver: one typed, deduplicated row per prime contract transaction in scope.
-- Runs unchanged on DuckDB (tests, snapshot) and Spark SQL (Databricks). Source view: bronze_prime_transactions
-- (columns as in the USAspending transaction download; schema contract enforced in code before this runs).
-- Rows listed in silver_rejects (built first) are excluded before any cast, so casts here cannot fail.
CREATE OR REPLACE TABLE silver_contract_transactions AS
WITH typed AS (
  SELECT
    contract_transaction_unique_key                          AS transaction_key,
    contract_award_unique_key                                AS award_key,
    award_id_piid                                            AS piid,
    parent_award_id_piid                                     AS parent_piid,
    CAST(modification_number AS VARCHAR)                     AS modification_number,
    TRY_CAST(action_date AS DATE)                            AS action_date,
    TRY_CAST(federal_action_obligation AS DECIMAL(18,2))     AS obligation,
    TRY_CAST(base_and_exercised_options_value AS DECIMAL(18,2)) AS base_and_exercised_options_value,
    TRY_CAST(base_and_all_options_value AS DECIMAL(18,2))    AS base_and_all_options_value,
    awarding_agency_code, awarding_agency_name, awarding_sub_agency_code, awarding_sub_agency_name,
    funding_agency_code, funding_agency_name,
    recipient_uei, recipient_name, recipient_parent_uei, recipient_parent_name,
    product_or_service_code                                  AS psc,
    product_or_service_code_description                      AS psc_description,
    naics_code                                               AS naics,
    naics_description,
    award_type_code, award_type,
    action_type_code, action_type,
    TRY_CAST(period_of_performance_start_date AS DATE)       AS pop_start,
    TRY_CAST(period_of_performance_current_end_date AS DATE) AS pop_current_end,
    TRY_CAST(last_modified_date AS DATE)                     AS last_modified_date,
    usaspending_permalink,
    _ingest_run_id, _ingest_agency_code, _ingest_fiscal_year, _ingest_file
  FROM bronze_prime_transactions b
  WHERE NOT EXISTS (SELECT 1 FROM silver_rejects r WHERE r.transaction_key IS NOT DISTINCT FROM b.contract_transaction_unique_key)
),
with_fy AS (
  SELECT *,
    CASE WHEN EXTRACT(MONTH FROM action_date) >= 10 THEN EXTRACT(YEAR FROM action_date) + 1
         ELSE EXTRACT(YEAR FROM action_date) END             AS fiscal_year,
    SUBSTRING(psc, 1, 1)                                     AS psc_class1,
    SUBSTRING(psc, 1, 2)                                     AS psc_class2,
    CASE WHEN psc LIKE 'D%' THEN 'IT services' WHEN psc LIKE '70%' THEN 'IT equipment and software' ELSE 'out of scope' END AS it_category
  FROM typed
),
deduped AS (
  SELECT * FROM with_fy
  QUALIFY ROW_NUMBER() OVER (PARTITION BY transaction_key ORDER BY _ingest_run_id DESC, last_modified_date DESC NULLS LAST) = 1
)
SELECT * FROM deduped;
