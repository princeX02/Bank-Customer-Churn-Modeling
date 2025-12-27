import streamlit as st
import pandas as pd
import joblib
import warnings

# 👇 add this block immediately after the imports
warnings.filterwarnings(
    "ignore",
    message="X does not have valid feature names, but LGBMClassifier was fitted with feature names",
)
# ==============================
# 1. LOAD MODEL BUNDLE
# ==============================
@st.cache_resource
def load_bundle():
    return joblib.load("models/best_churn_model.pkl")

bundle = load_bundle()
model = bundle["model"]
preprocessor = bundle["preprocessor"]

# ==============================
# 2. PAGE CONFIG + THEME
# ==============================
st.divider()
st.set_page_config(
    page_title="Bank Churn Predictor",
    page_icon="🏦",
    layout="wide"
)

# Custom CSS for nicer UI
st.markdown(
    """
    <style>
    .main {
        background-color: #0f172a;
        color: #e5e7eb;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    .big-title {
        font-size: 32px;
        font-weight: 700;
        color: #fbbf24;
    }
    .sub-title {
        font-size: 16px;
        color: #9ca3af;
    }
    .card {
        background-color: #020617;
        padding: 18px 18px 10px 18px;
        border-radius: 12px;
        border: 1px solid #1f2937;
    }
    .metric-card {
        background-color: #020617;
        padding: 16px;
        border-radius: 12px;
        border: 1px solid #374151;
    }
    .metric-label {
        font-size: 13px;
        color: #9ca3af;
    }
    .metric-value {
        font-size: 22px;
        font-weight: 700;
        color: #f9fafb;
    }
    .metric-sub {
        font-size: 12px;
        color: #6b7280;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==============================
# 3. HEADER
# ==============================
col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.markdown("### 🏦")
with col_title:
    st.markdown('<div class="big-title">Bank Customer Churn Predictor</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-title">Interactive dashboard to estimate churn probability and recommended business action.</div>',
        unsafe_allow_html=True,
    )

st.markdown("---")

# ==============================
# 4. SIDEBAR – INPUT FORM
# ==============================
st.sidebar.markdown("### 🧾 Customer Profile")

credit_score = st.sidebar.slider("Credit Score", 300, 900, 650)
age = st.sidebar.slider("Age", 18, 92, 40)
tenure = st.sidebar.slider("Tenure (Years with Bank)", 0, 10, 3)
balance = st.sidebar.slider("Account Balance ($)", 0.0, 250000.0, 60000.0, step=1000.0)
num_products = st.sidebar.slider("Number of Products", 1, 4, 2)
salary = st.sidebar.slider("Estimated Salary ($)", 0.0, 200000.0, 50000.0, step=1000.0)

st.sidebar.markdown("---")
geography = st.sidebar.selectbox("Geography", ["France", "Spain", "Germany"])
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
has_crcard = st.sidebar.radio("Has Credit Card", ["Yes", "No"], horizontal=True)
is_active = st.sidebar.radio("Is Active Member", ["Yes", "No"], horizontal=True)

predict_clicked = st.sidebar.button("🔮 Predict Churn Risk", use_container_width=True)

# ==============================
# 5. BUILD INPUT DATAFRAME
# ==============================
customer_dict = {
    "CreditScore": credit_score,
    "Geography": geography,
    "Gender": gender,
    "Age": age,
    "Tenure": tenure,
    "Balance": balance,
    "NumOfProducts": num_products,
    "HasCrCard": 1 if has_crcard == "Yes" else 0,
    "IsActiveMember": 1 if is_active == "Yes" else 0,
    "EstimatedSalary": salary,
}
df_input = pd.DataFrame([customer_dict])

# Engineered features – must match training
df_input["BalancePerProduct"] = df_input["Balance"] / (df_input["NumOfProducts"] + 1)
df_input["IsSenior"] = (df_input["Age"] >= 50).astype(int)

bins = [0, 580, 650, 720, 1000]
labels = [0, 1, 2, 3]
df_input["CreditRisk"] = pd.cut(
    df_input["CreditScore"], bins=bins, labels=labels, include_lowest=True
).astype(int)

# ==============================
# 6. MAIN LAYOUT
# ==============================
left, right = st.columns([2, 3])

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### 👤 Customer Snapshot")

    info1, info2 = st.columns(2)
    with info1:
        st.write(f"- **Age:** {age}")
        st.write(f"- **Country:** {geography}")
        st.write(f"- **Gender:** {gender}")
    with info2:
        st.write(f"- **Balance:** ${balance:,.0f}")
        st.write(f"- **Products:** {num_products}")
        st.write(f"- **Tenure:** {tenure} years")

    st.write("")
    st.markdown("#### 🧮 Engineered Features")
    ef1, ef2 = st.columns(2)
    with ef1:
        st.write(f"- Balance / Products: ${df_input['BalancePerProduct'].iloc[0]:,.0f}")
        st.write(f"- Senior Flag: {int(df_input['IsSenior'].iloc[0])}")
    with ef2:
        st.write(f"- Credit Risk Bucket: {int(df_input['CreditRisk'].iloc[0])}")
        st.write(f"- Active Member: {1 if is_active == 'Yes' else 0}")

    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### 📊 Churn Prediction")

    if predict_clicked:
        X_processed = preprocessor.transform(df_input)
        prob = model.predict_proba(X_processed)[0, 1]
        churn_percent = prob * 100

        if prob >= 0.7:
            risk_label = "High Risk"
            risk_color = "🔴"
            action = "Strong retention campaign required (discounts, calls, offers)."
        elif prob >= 0.4:
            risk_label = "Medium Risk"
            risk_color = "🟡"
            action = "Monitor closely and send engagement messages."
        else:
            risk_label = "Low Risk"
            risk_color = "🟢"
            action = "Customer is likely to stay; maintain current service level."

        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">Churn Probability</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{churn_percent:.1f}%</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-sub">Predicted by best LightGBM model</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with m2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">Risk Level</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{risk_color} {risk_label}</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-sub">Based on probability thresholds</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with m3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">Recommended Action</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-value">Next Step</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-sub">{action}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)   
    else:
        st.info("Use the controls in the left sidebar and click **Predict Churn Risk** to see the results.")
        st.markdown("</div>", unsafe_allow_html=True)
