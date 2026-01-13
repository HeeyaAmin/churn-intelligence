import os
import pandas as pd
from sqlalchemy import create_engine

# Update if your Postgres user is not your mac username
DB_URL = "postgresql+psycopg2://heeyaamin@localhost:5432/churn_db"
CSV_PATH = "data/telco_churn.csv"

def main():
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"CSV file not found at path: {CSV_PATH}")
    df = pd.read_csv(CSV_PATH)

    # Standardize common Telco churn column names (if needed)
    rename_map = {
    "customerID": "customer_id",
    "SeniorCitizen": "senior_citizen",
    "Partner": "partner",
    "Dependents": "dependents",
    "tenure": "tenure",
    "PhoneService": "phone_service",
    "MultipleLines": "multiple_lines",
    "InternetService": "internet_service",
    "OnlineSecurity": "online_security",
    "OnlineBackup": "online_backup",
    "DeviceProtection": "device_protection",
    "TechSupport": "tech_support",
    "StreamingTV": "streaming_tv",
    "StreamingMovies": "streaming_movies",
    "Contract": "contract",
    "PaperlessBilling": "paperless_billing",
    "PaymentMethod": "payment_method",
    "MonthlyCharges": "monthly_charges",
    "TotalCharges": "total_charges",
    "Churn": "churn"
}

    df = df.rename(columns=rename_map)

    expected_cols = [
        "customer_id","gender","senior_citizen","partner","dependents","tenure",
        "phone_service","multiple_lines","internet_service","online_security","online_backup",
        "device_protection","tech_support","streaming_tv","streaming_movies","contract",
        "paperless_billing","payment_method","monthly_charges","total_charges","churn"
    ]
    missing = [c for c in expected_cols if c not in df.columns]
    if missing:
        raise ValueError(f"CSV is missing expected columns: {missing}")

    df = df[expected_cols]

    engine = create_engine(DB_URL)

    # Overwrite customers_raw each run
    df.to_sql("customers_raw", engine, if_exists="replace", index=False)

    print("Loaded customers_raw rows:", len(df))
    print("Done.")

if __name__ == "__main__":
    main()