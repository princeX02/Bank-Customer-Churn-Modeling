import streamlit as st
import requests

API_URL = "http://127.0.0.1:8001/predict"

st.title("🏦 Bank Customer Churn Predictor")

# Sidebar inputs
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
        response = requests.post(API_URL, json=payload, timeout=10)  # timeout to avoid hanging
        response.raise_for_status()  # Raise exception if HTTP status != 200
        data = response.json()

        st.subheader("📊 Prediction Result")
        st.write(f"**Churn Probability:** {data['churn_percentage']}%")
        st.write(f"**Risk Level:** {data['risk_level']}")
        st.write(f"**Recommended Action:** {data['recommended_action']}")

    except requests.exceptions.Timeout:
        st.error("⏰ Backend timed out. Make sure FastAPI is running and reachable.")
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to backend. Check FastAPI URL and port.")
    except requests.exceptions.HTTPError as e:
        st.error(f"⚠️ HTTP Error: {e}")
    except Exception as e:
        st.error(f"💥 Unexpected error: {e}")
