# Bank Customer Churn Prediction

## Overview
This project predicts customer churn for a bank using machine learning models. The goal is to identify customers likely to leave the bank so retention strategies can be implemented.

## Dataset
- **Source**: Churn_Modelling.csv
- **Records**: [X rows]
- **Features**: Customer demographics, account information, activity metrics
- **Target**: Exited (1 = Churned, 0 = Retained)

## Project Structure
```
├── data/
│   └── Churn_Modelling.csv
├── notebooks/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_modeling_xgboost.ipynb
│   └── 05_explainability_shap.ipynb
├── app.py
├── index.py
├── requirements.txt
└── README.md
```

## Installation
```bash
pip install -r requirements.txt
```

## Usage
1. Run notebooks in order (01 → 05)
2. Each notebook is self-contained and documented

## Methodology
1. **Data Cleaning**: Handle missing values, outliers
2. **EDA**: Analyze patterns and correlations
3. **Feature Engineering**: Create new features, encoding
4. **Modeling**: XGBoost, Random Forest, Logistic Regression
5. **Explainability**: SHAP values for model interpretation

## Algorithms Used
- logistic regression
- random forest
- XGBoost
- Smooth based model

## Results
- **Best Model**: XGBoost
- **Accuracy**: XX%
- **AUC-ROC**: XX
- **Key Features**: [Top 3 important features]

## Technologies
- Python 3.x
- pandas, numpy, scikit-learn
- xgboost
- matplotlib, seaborn
- shap

## Explanation
“I used Logistic Regression for interpretability, Random Forest for non-linear patterns,   XGBoost for high performance, and SMOTE to handle class imbalance.
I evaluated all models using ROC-AUC and recall because missing a churn customer has high business cost.
XGBoost performed best, but I balanced performance with explainability based on business needs.”
## Author
- Prince Chaudhary
- Email:princechaudhary@gmail.com
- GitHub: [github.com/princechaudhary](https://github.com/princechaudhary)
- LinkedIn: [linkedin.com/in/prince-chaudhary](https://www.linkedin.com/in/prince-chaudhary/)

