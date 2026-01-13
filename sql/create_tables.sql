-- sql creating tables for customer churn prediction
DROP TABLE IF EXISTS churn_predictions;
DROP TABLE IF EXISTS customers_features;
DROP TABLE IF EXISTS customers_raw;

-- raw table (matches csv columns loosely, keep as TEXT for easy load)
CREATE TABLE customers_raw (
    customer_id TEXT,
    gender TEXT,
    senior_citizen TEXT,
    partner TEXT,
    dependents TEXT,
    tenure TEXT,
    phone_service TEXT,
    multiple_lines TEXT,
    internet_service TEXT,
    online_security TEXT,
    online_backup TEXT,
    device_protection TEXT,
    tech_support TEXT,
    streaming_tv TEXT,
    streaming_movies TEXT,
    contract TEXT,
    paperless_billing TEXT,
    payment_method TEXT,
    monthly_charges TEXT,
    total_charges TEXT,
    churn TEXT 
);

-- features table (cleaned and typed data for modeling)
CREATE TABLE customers_features (
  customer_id TEXT PRIMARY KEY,
  tenure INT,
  monthly_charges NUMERIC(10,2),
  total_charges NUMERIC(12,2),

  senior_citizen INT,                 -- 0/1
  has_partner INT,                    -- 0/1
  has_dependents INT,                 -- 0/1
  paperless_billing INT,              -- 0/1

  contract_type TEXT,
  internet_service TEXT,
  payment_method TEXT,

  churn_label INT                     -- 0/1
);

-- predictions table (store model predictions)
-- 3) Predictions table (Power BI reads this!)
CREATE TABLE churn_predictions (
  customer_id TEXT PRIMARY KEY,
  churn_probability NUMERIC(6,5),
  risk_bucket TEXT,
  model_name TEXT,
  model_version TEXT,
  prediction_date TIMESTAMP DEFAULT NOW()
);
