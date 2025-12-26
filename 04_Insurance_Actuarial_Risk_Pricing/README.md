# 🛡️ Life Insurance: Actuarial Risk & Pricing Analytics

![Python](https://img.shields.io/badge/Python-Actuarial%20Modeling-blue)
![Power BI](https://img.shields.io/badge/PowerBI-Risk%20Dashboard-yellow)
![Industry](https://img.shields.io/badge/Industry-Insurance%20(InsurTech)-red)

## 📋 Executive Summary
In the Life Insurance industry, profitability depends on accurately pricing mortality risk and retaining policyholders.

This project implements an **Actuarial Risk Dashboard** that analyzes a portfolio of 12,000 policies. It visualizes the correlation between health factors (Smoking, BMI) and pricing premiums, while monitoring critical retention KPIs like **Lapse Rate**.

## 💼 Business Problem
* **Risk Pricing:** Ensuring that high-risk segments (e.g., Smokers, Older demographics) are paying adequate premiums to cover future claims.
* **Lapse Risk:** Identifying which products suffer from high cancellation rates (Lapse), which destroys long-term value for the insurer.

## 🛠️ Technical Solution
1.  **Actuarial Data Simulation (Python):** Generated a synthetic portfolio modeling real-world insurance dynamics:
    * *Mortality Tables Logic:* Premiums increase exponentially with age.
    * *Underwriting Factors:* Smokers pay ~2.5x higher premiums.
    * *Product Mix:* Term Life (10/20/30Y) vs. Whole Life.
2.  **Risk Analysis Dashboard (Power BI):**
    * **Pricing Curve:** A scatter plot validating the exponential relationship between Age and Premium for Whole Life products.
    * **Retention Analysis:** Breakdown of Lapse Rates by product type, revealing higher attrition in expensive "Whole Life" policies.

## 📊 Key Insights
* **The Smoker Penalty:** The analysis confirms a **140% premium increase** for smokers compared to non-smokers, validating the underwriting model.
* **Lapse Risk:** "Whole Life" policies show the highest Lapse Rate (>8%), suggesting a need for better customer education or flexible payment options to improve retention.
* **Total Exposure:** The portfolio manages **$3.39 Billion** in active coverage risk.

## ⚙️ How to Run
1.  Run the simulation script:
    ```bash
    python generate_life_insurance_data.py
    ```
2.  Open `Life_Insurance_Analytics.pbix` in Power BI.

---
### Author
**Glauber Rocha**
*Finance & Analytics Specialist*
