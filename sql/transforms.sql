-- sql/transforms.sql
-- Clean + type data from customers_raw into customers_features

TRUNCATE TABLE customers_features;

INSERT INTO customers_features (
  customer_id,
  tenure,
  monthly_charges,
  total_charges,
  senior_citizen,
  has_partner,
  has_dependents,
  paperless_billing,
  contract_type,
  internet_service,
  payment_method,
  churn_label
)
SELECT
  customer_id,

  -- Force to text first, then clean/cast
  NULLIF(BTRIM(tenure::TEXT), '')::INT AS tenure,

  NULLIF(BTRIM(monthly_charges::TEXT), '')::NUMERIC(10,2) AS monthly_charges,

  NULLIF(BTRIM(total_charges::TEXT), '')::NUMERIC(12,2) AS total_charges,

  -- senior_citizen can be 0/1 or Yes/No depending on how it got loaded; normalize safely
  CASE
    WHEN LOWER(BTRIM(senior_citizen::TEXT)) IN ('1', 'yes', 'true') THEN 1
    ELSE 0
  END AS senior_citizen,

  CASE WHEN LOWER(BTRIM(partner::TEXT)) = 'yes' THEN 1 ELSE 0 END AS has_partner,
  CASE WHEN LOWER(BTRIM(dependents::TEXT)) = 'yes' THEN 1 ELSE 0 END AS has_dependents,
  CASE WHEN LOWER(BTRIM(paperless_billing::TEXT)) = 'yes' THEN 1 ELSE 0 END AS paperless_billing,

  BTRIM(contract::TEXT) AS contract_type,
  BTRIM(internet_service::TEXT) AS internet_service,
  BTRIM(payment_method::TEXT) AS payment_method,

  CASE WHEN LOWER(BTRIM(churn::TEXT)) = 'yes' THEN 1 ELSE 0 END AS churn_label
FROM customers_raw;