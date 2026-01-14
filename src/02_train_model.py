import os
import joblib
import pandas as pd
from sqlalchemy import create_engine

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.metrics import roc_auc_score, classification_report
from sklearn.linear_model import LogisticRegression

DB_URL = "postgresql+psycopg2://heeyaamin@localhost:5432/churn_db"

ARTIFACT_DIR = "artifacts"
MODEL_PATH = os.path.join(ARTIFACT_DIR, "churn_model.joblib")

def main():
    os.makedirs(ARTIFACT_DIR, exist_ok=True)

    engine = create_engine(DB_URL)

    df = pd.read_sql("SELECT * FROM customers_features;", engine)

    # Drop rows missing target or critical numeric fields (keep it simple)
    df = df.dropna(subset=["churn_label", "tenure", "monthly_charges"])

    X = df.drop(columns=["churn_label", "customer_id"])
    y = df["churn_label"].astype(int)

    # Identify feature types
    numeric_features = ["tenure", "monthly_charges", "total_charges",
                        "senior_citizen", "has_partner", "has_dependents", "paperless_billing"]
    categorical_features = ["contract_type", "internet_service", "payment_method"]

    # Preprocessing
    numeric_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median"))
    ])

    categorical_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore"))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ],
        remainder="drop"
    )

    # Model (baseline but strong + interpretable)
    clf = LogisticRegression(max_iter=2000)

    model = Pipeline(steps=[
        ("preprocess", preprocessor),
        ("clf", clf)
    ])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model.fit(X_train, y_train)

    # Evaluate
    probs = model.predict_proba(X_test)[:, 1]
    preds = (probs >= 0.5).astype(int)

    auc = roc_auc_score(y_test, probs)
    print(f"ROC-AUC: {auc:.4f}")
    print("\nClassification report:\n")
    print(classification_report(y_test, preds))

    # Save model
    joblib.dump(model, MODEL_PATH)
    print(f"\nSaved model to: {MODEL_PATH}")

if __name__ == "__main__":
    main()