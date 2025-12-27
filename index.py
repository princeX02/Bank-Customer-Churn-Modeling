import streamlit as st
import requests

# ------------------------------
# Page config
# ------------------------------
st.set_page_config(
    page_title="Bank Churn Predictor",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 Bank Customer Churn Predictor")

# ------------------------------
# Sidebar - Input form
# ------------------------------
st.sidebar.header("Customer Profile")

credit_score = st.sidebar.slider("Credit Score", 300, 900, 650)
age = st.sidebar.slider("Age", 18, 92, 40)
tenure = st.sidebar.slider("Tenure (Years with Bank)", 0, 10, 3)
balance = st.sidebar.slider("Account Balance ($)", 0.0, 250000.0, 60000.0, step=1000.0)
num_products = st.sidebar.slider("Number of Products", 1, 4, 2)
salary = st.sidebar.slider("Estimated Salary ($)", 0.0, 200000.0, 50000.0, step=1000.0)

geography = st.sidebar.selectbox("Geography", ["France", "Spain", "Germany"])
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
has_crcard = st.sidebar.radio("Has Credit Card", ["Yes", "No"], horizontal=True)
is_active = st.sidebar.radio("Is Active Member", ["Yes", "No"], horizontal=True)

predict_clicked = st.sidebar.button("🔮 Predict Churn Risk")

# ------------------------------
# Make API call when button clicked
# ------------------------------
if predict_clicked:
    payload = {
        "CreditScore": credit_score,
        "Geography": geography,
        "Gender": gender,
        "Age": age,
        "Tenure": tenure,
        "Balance": balance,
        "NumOfProducts": num_products,
        "HasCrCard": 1 if has_crcard == "Yes" else 0,
        "IsActiveMember": 1 if is_active == "Yes" else 0,
        "EstimatedSalary": salary
    }

    try:
        response = requests.post("http://127.0.0.1:8001/predict", json=payload)
        data = response.json()

        st.subheader("📊 Prediction Result")
        st.write(f"**Churn Probability:** {data['churn_percentage']}%")
        st.write(f"**Risk Level:** {data['risk_level']}")
        st.write(f"**Recommended Action:** {data['recommended_action']}")

    except Exception as e:
        st.error(f"Error connecting to backend: {e}")
