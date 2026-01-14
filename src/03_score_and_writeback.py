import os
import joblib
import pandas as pd
from sqlalchemy import create_engine, text

DB_URL = "postgresql+psycopg2://heeyaamin@localhost:5432/churn_db"

MODEL_PATH = "artifacts/churn_model.joblib"
MODEL_NAME = "LogisticRegression"
MODEL_VERSION = "v1"

def risk_bucket(p: float) -> str:
    # Simple, explainable buckets for business users
    if p >= 0.70:
        return "High"
    if p >= 0.40:
        return "Medium"
    return "Low"

def main():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model not found at {MODEL_PATH}. Run 02_train_model.py first.")

    engine = create_engine(DB_URL)

    df = pd.read_sql("SELECT * FROM customers_features;", engine)

    # Keep customer_id for writeback
    customer_ids = df["customer_id"].copy()

    X = df.drop(columns=["churn_label", "customer_id"])

    model = joblib.load(MODEL_PATH)

    probs = model.predict_proba(X)[:, 1]
    out = pd.DataFrame({
        "customer_id": customer_ids,
        "churn_probability": probs,
        "risk_bucket": [risk_bucket(p) for p in probs],
        "model_name": MODEL_NAME,
        "model_version": MODEL_VERSION,
    })

    # Write predictions:
    # We'll TRUNCATE then insert fresh predictions each run.
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE churn_predictions;"))

    out.to_sql("churn_predictions", engine, if_exists="append", index=False)

    print("Wrote predictions:", len(out))
    print(out.head(10))

if __name__ == "__main__":
    main()