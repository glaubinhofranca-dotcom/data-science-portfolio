# 🎓 FRIS: Student Federal Loan Default Predictor

[![Live App](https://img.shields.io/badge/Live%20App-Hugging%20Face%20Spaces-yellow)](https://huggingface.co/spaces/glaubinhofranca-dotcom/fris-predictive-risk-framework)
[![Repository](https://img.shields.io/badge/Full%20Repository-GitHub-black)](https://github.com/glaubinhofranca-dotcom/fris-predictive-risk-framework)

## 📌 Project Overview

Higher education institutions face a critical challenge: **federal student loan defaults** damage both students and the institution's Title IV eligibility. Most financial aid offices react after delinquency occurs — too late to prevent defaults.

**FRIS (Financial Risk Intelligence System)** is a production ML framework deployed at **New England College** that predicts federal loan default risk from institutional SIS data. It enables proactive interventions before delinquency escalates to the federal 270-day default threshold.

## 💼 Business Problem

- **Issue:** 7.5% default rate across 1,302 borrowers — reactive monitoring fails to prevent escalation
- **Regulatory Risk:** Cohort Default Rate (CDR) violations threaten Title IV (federal financial aid) eligibility
- **Goal:** Predict which students will default and enable targeted counseling interventions before default occurs
- **Constraint:** FERPA compliance — no real student data can leave institutional systems

## 🛠️ Tech Stack

- **Language:** Python
- **ML:** scikit-learn (Random Forest, Gradient Boosting, Logistic Regression)
- **Backend:** FastAPI + Server-Sent Events (SSE) for real-time pipeline streaming
- **Frontend:** Vanilla JS + Chart.js interactive dashboard
- **Deployment:** Docker + Hugging Face Spaces (auto-deployed via GitHub Actions)
- **SIS Adapters:** Banner, Workday Student, PeopleSoft, Colleague

## 📊 Methodology

1. **Data Ingestion:** Upload institutional CSV — SIS profile auto-maps columns (Banner/Workday/PeopleSoft/Colleague)
2. **ETL & Feature Engineering:** Normalizes GPA, loan balances, payment plans, enrollment status; defines target as `Days_Delinquent > 270` (34 CFR § 682.200)
3. **EDA:** Distributions, missing value audit, correlation with default flag — streamed live to dashboard
4. **Segmentation:** Default rates across 8 dimensions: GPA buckets, student type, graduation status, program, campus
5. **Modeling:** 5-fold Stratified Cross-Validation with `class_weight="balanced"` across 3 classifiers; Random Forest selected as best model
6. **Results Dashboard:** Feature importance, subgroup AUC, segmentation charts — all rendered via SSE stream

## 📈 Key Results

| Metric | Value |
|--------|-------|
| **AUC-ROC** | **0.772 ± 0.055** |
| F1 Score | 0.310 |
| Recall | 0.499 |
| Accuracy | 0.826 |

**Subgroup performance:**
- Undergraduate (n=992): AUC = **0.796**
- Graduate (n=310): AUC = **0.564**

**Top predictors (NEC run):**
- Payment plan → 18.6%
- Academic program → 16.1%
- GPA → 11.9%

**Critical Policy Finding:** Students enrolled in Income-Driven Repayment (IDR) plans default at **0.7%** vs. **9.6%** for non-IDR — a **13.7× difference**, identifying IDR enrollment counseling as the single highest-impact intervention.

## 🏫 Multi-SIS Support

| SIS | Coverage |
|-----|----------|
| Banner / Ellucian | ~1,200 US institutions |
| Workday Student | Enterprise cloud SIS |
| PeopleSoft / Oracle | Large public universities |
| Colleague / Ellucian | ~700 US institutions |

## 🔒 Data Privacy & Compliance

- No real student data included in this repository
- Session data isolated in Docker volumes (excluded from git)
- FERPA-compliant architecture
- Full repo: [fris-predictive-risk-framework](https://github.com/glaubinhofranca-dotcom/fris-predictive-risk-framework)

## 🚀 How to Run

```bash
# With Docker
docker compose up --build
# Open http://localhost:7860

# Locally
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 7860
```
