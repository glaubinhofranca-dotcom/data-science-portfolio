# 🏦 Credit Risk Scoring & Regulatory Modeling

## 📌 Project Overview
In the banking industry, "Black Box" models are often rejected by regulators due to lack of interpretability. This project builds a **Basel-compliant Application Scorecard** using Logistic Regression to predict the **Probability of Default (PD)** of loan applicants.

Beyond binary classification, the engine calculates the **Expected Loss (EL)** and maps the risk probability to a standard **FICO-like Credit Score (300-850)**, bridging the gap between Data Science and Financial Risk Management.

## 💼 Business Problem
- **Issue:** Minimizing NPL (Non-Performing Loans) while maintaining a competitive approval rate.
- **Goal:** Build a transparent decision engine to Approve/Reject loans based on quantitative risk.
- **Regulatory Requirement:** The model must be interpretable to justify adverse actions (loan denials) to customers and auditors.

## 🛠️ Tech Stack
- **Language:** Python
- **Libraries:** Scikit-Learn (Pipeline, ColumnTransformer), Pandas, NumPy.
- **Modeling:** Logistic Regression (Selected for regulatory compliance).
- **Visualization:** Power BI (Portfolio Health Dashboard).

## 📊 Methodology
1. **Data Simulation:** Generated a dataset of 10,000 applicants with realistic features like *Debt-to-Income (DTI)* ratio, *Home Ownership*, and *Credit History*.
2. **Feature Engineering:** Calculated financial ratios critical for solvency analysis.
3. **Modeling:** Trained a Logistic Regression model with balanced class weights to handle default rarity.
4. **Scorecard Calibration:**
   - Calibrated **Probability of Default (PD)**.
   - Scaled Log-Odds to a 300-850 point range.
   - Calculated **Expected Loss (EL = PD × LGD × EAD)** assuming a 60% LGD.

## 📈 Key Results
- **Model Accuracy:** Achieved an ROC-AUC > 0.75.
- **Risk Segmentation:** Successfully stratified the portfolio into risk buckets (Poor to Exceptional).
- **Financial Impact:** The Power BI dashboard allows the CRO (Chief Risk Officer) to simulate how changing the "Cut-off Score" impacts the bank's provisions (Expected Loss).

## 🚀 How to Run
1. Run the script: `python finance_project_credit_risk.py`
2. The script will export `credit_risk_powerbi.csv`.
3. Import the CSV into Power BI to analyze the Risk Exposure.
