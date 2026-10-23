-- Rows that cannot be used; kept with a reason so counts reconcile (bronze = silver + rejects + duplicates).
CREATE OR REPLACE TABLE silver_rejects AS
SELECT contract_transaction_unique_key AS transaction_key, _ingest_run_id, _ingest_agency_code, _ingest_fiscal_year,
  CASE
    WHEN contract_transaction_unique_key IS NULL OR contract_transaction_unique_key = '' THEN 'missing transaction key'
    WHEN TRY_CAST(action_date AS DATE) IS NULL THEN 'unparseable action_date'
    WHEN TRY_CAST(federal_action_obligation AS DECIMAL(18,2)) IS NULL THEN 'unparseable obligation'
    WHEN product_or_service_code IS NULL OR NOT (product_or_service_code LIKE 'D%' OR product_or_service_code LIKE '70%') THEN 'psc out of scope'
    WHEN award_type_code NOT IN ('A','B','C','D') THEN 'not a contract award type'
  END AS reason
FROM bronze_prime_transactions
WHERE contract_transaction_unique_key IS NULL OR contract_transaction_unique_key = ''
   OR TRY_CAST(action_date AS DATE) IS NULL
   OR TRY_CAST(federal_action_obligation AS DECIMAL(18,2)) IS NULL
   OR product_or_service_code IS NULL OR NOT (product_or_service_code LIKE 'D%' OR product_or_service_code LIKE '70%')
   OR award_type_code NOT IN ('A','B','C','D');
