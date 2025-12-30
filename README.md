# Bank Customer Churn Prediction

## Overview
This project predicts customer churn for a bank using machine learning models. The goal is to identify customers likely to leave the bank so retention strategies can be implemented.

## Dataset
- **Source**: `Churn_Modelling.csv`
- **Records**: [X rows]
- **Features**: Customer demographics, account information, activity metrics
- **Target**: `Exited` (1 = Churned, 0 = Retained)

## Project Structure
├── data/
│ └── Churn_Modelling.csv
├── notebooks/
│ ├── 01_data_cleaning.ipynb
│ ├── 02_eda.ipynb
│ ├── 03_feature_engineering.ipynb
│ ├── 04_modeling_xgboost.ipynb
│ └── 05_explainability_shap.ipynb
├── backend/
│ ├── app.py
| ├── Dockerfile
│ └── requirements.txt
├── frontend/
│ ├── index.py
│ ├── Dockerfile
│ └── requirements.txt
├── docker-compose.yml
└── README.md


## Installation

### Local setup
```bash
# Clone the repo
git clone <https://github.com/princeX02/Bank-Customer-Churn-Modeling.git>
cd Bank-Customer-Churn-Prediction

# Install Python dependencies
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt


# Build and run using Docker Compose
docker-compose up --build
Backend (FastAPI): http://localhost:8000/predict
Frontend (Streamlit): http://localhost:8501

