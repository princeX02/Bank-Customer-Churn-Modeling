from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
import warnings

warnings.filterwarnings("ignore")

# Load model bundle
bundle = joblib.load("models/best_churn_model.pkl")
model = bundle["model"]
preprocessor = bundle["preprocessor"]

app = FastAPI(title="Bank Customer Churn API", version="1.0")

class CustomerInput(BaseModel):
    CreditScore: int
    Geography: str
    Gender: str
    Age: int
    Tenure: int
    Balance: float
    NumOfProducts: int
    HasCrCard: int
    IsActiveMember: int
    EstimatedSalary: float

@app.get("/")
def home():
    return {"status": "FastAPI is running"}

@app.post("/predict")
def predict_churn(data: CustomerInput):
    df = pd.DataFrame([data.dict()])
    df["BalancePerProduct"] = df["Balance"] / (df["NumOfProducts"] + 1)
    df["IsSenior"] = (df["Age"] >= 50).astype(int)

    bins = [0, 580, 650, 720, 1000]
    labels = [0, 1, 2, 3]
    df["CreditRisk"] = pd.cut(
        df["CreditScore"], bins=bins, labels=labels, include_lowest=True
    ).astype(int)

    X_processed = preprocessor.transform(df)
    prob = model.predict_proba(X_processed)[0, 1]

    if prob >= 0.7:
        risk = "High Risk"
        action = "Immediate retention action required"
    elif prob >= 0.4:
        risk = "Medium Risk"
        action = "Monitor and engage customer"
    else:
        risk = "Low Risk"
        action = "Customer likely to stay"

    return {
        "churn_probability": round(prob, 4),
        "churn_percentage": round(prob * 100, 2),
        "risk_level": risk,
        "recommended_action": action
    }
