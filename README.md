# 🏦 Bank Customer Churn Prediction

## 📌 Overview
Customer churn is a major concern for banks and financial institutions. This project uses **machine learning techniques** to predict whether a customer is likely to leave the bank based on demographic, behavioral, and account-related features.

The solution helps businesses:
- Identify high-risk customers  
- Take proactive retention measures  
- Improve customer lifetime value  

---

## 📊 Dataset
- **Source**: `Churn_Modelling.csv`
- **Number of Records**: ~10,000
- **Features**:
  - Customer demographics (Age, Gender, Geography)
  - Account information (Balance, Credit Score, Tenure)
  - Activity metrics (Number of Products, IsActiveMember)
- **Target Variable**:
  - `Exited`
    - `1` → Customer churned
    - `0` → Customer retained

---

## 🗂️ Project Structure
```bash
Bank-Customer-Churn-Modeling/
│
├── data/
│   └── Churn_Modelling.csv
│
├── notebooks/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_modeling_xgboost.ipynb
│   └── 05_explainability_shap.ipynb
│
├── backend/
│   ├── app.py                  # FastAPI backend
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── index.py                # Streamlit frontend
│   ├── Dockerfile
│   └── requirements.txt
│
├── docker-compose.yml
└── README.md

```

##      Installation & Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/princeX02/Bank-Customer-Churn-Modeling.git
   cd Bank-Customer-Churn-Modeling
   ```  
2. **Run with Docker Compose**:
   Ensure you have Docker and Docker Compose installed. Then run:
   ```bash
   docker-compose up --build
   or
   docker compose -f docker-compose.yml up
   ```

3. **Access the Application**:
   - Frontend: Open your browser and navigate to `http://localhost:8501`
   - Backend API: Accessible at `http://localhost:8000/predict`
