import streamlit as st
import requests
import pandas as pd

# API_URL = "http://127.0.0.1:8001/predict"
API_URL = "https://bank-customer-churn-modeling-1.onrender.com/predict"

st.set_page_config(page_title="Bank Churn Predictor", page_icon="🏦", layout="wide")
st.title("🏦 Bank Customer Churn Predictor")

# Sidebar Inputs
st.sidebar.header("Customer Profile")
credit_score = st.sidebar.slider("Credit Score", 300, 900, 650)
age = st.sidebar.slider("Age", 18, 92, 40)
tenure = st.sidebar.slider("Tenure", 0, 10, 3)
balance = st.sidebar.slider("Account Balance ($)", 0.0, 250000.0, 60000.0, step=1000.0)
num_products = st.sidebar.slider("Number of Products", 1, 4, 2)
salary = st.sidebar.slider("Estimated Salary ($)", 0.0, 200000.0, 50000.0, step=1000.0)
geography = st.sidebar.selectbox("Geography", ["France", "Spain", "Germany"])
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
has_crcard = st.sidebar.radio("Has Credit Card", ["Yes", "No"], horizontal=True)
is_active = st.sidebar.radio("Is Active Member", ["Yes", "No"], horizontal=True)

predict_clicked = st.sidebar.button("🔮 Predict Churn Risk")

if predict_clicked:
    payload = {
        "CreditScore": int(credit_score),
        "Geography": str(geography),
        "Gender": str(gender),
        "Age": int(age),
        "Tenure": int(tenure),
        "Balance": float(balance),
        "NumOfProducts": int(num_products),
        "HasCrCard": 1 if has_crcard == "Yes" else 0,
        "IsActiveMember": 1 if is_active == "Yes" else 0,
        "EstimatedSalary": float(salary)
    }

    try:
        response = requests.post(API_URL, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()

        left, right = st.columns([2, 3])

        with left:
            st.subheader("👤 Customer Snapshot")
            st.markdown(f"- **Age:** {age}")
            st.markdown(f"- **Gender:** {gender}")
            st.markdown(f"- **Country:** {geography}")
            st.markdown(f"- **Balance:** ${balance:,.0f}")
            st.markdown(f"- **Products:** {num_products}")
            st.markdown(f"- **Tenure:** {tenure} years")

            # Engineered features
            balance_per_product = balance / (num_products + 1)
            is_senior = 1 if age >= 50 else 0
            credit_risk = pd.cut([credit_score], bins=[0,580,650,720,1000], labels=[0,1,2,3])[0]
            st.markdown(f"- **Balance / Product:** ${balance_per_product:,.0f}")
            st.markdown(f"- **Senior Flag:** {is_senior}")
            st.markdown(f"- **Credit Risk Bucket:** {credit_risk}")

        with right:
            st.subheader("📊 Churn Prediction")
            prob = data['churn_percentage']
            risk = data['risk_level']
            action = data['recommended_action']

            # Colored risk indicator
            color = "🟢" if risk=="Low Risk" else ("🟡" if risk=="Medium Risk" else "🔴")
            st.markdown(f"**Churn Probability:** {prob}%")
            st.markdown(f"**Risk Level:** {color} {risk}")
            st.markdown(f"**Recommended Action:** {action}")

    except requests.exceptions.Timeout:
        st.error("⏰ Backend timed out. Make sure FastAPI is running.")
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to backend.")
    except Exception as e:
        st.error(f"💥 Unexpected error: {e}")
