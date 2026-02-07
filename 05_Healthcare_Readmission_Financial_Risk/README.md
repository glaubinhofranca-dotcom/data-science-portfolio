# 🏥 Healthcare Analytics: Readmission & Financial Risk Model

![Python](https://img.shields.io/badge/Python-Synthetic%20Data-blue)
![Power BI](https://img.shields.io/badge/PowerBI-Dashboard-yellow)
![Domain](https://img.shields.io/badge/Industry-Healthcare%20USA-red)

## 📋 Executive Summary
In the US Healthcare system, **Hospital Readmissions** (patients returning within 30 days) are a major driver of financial penalties (HRRP) and revenue loss.

This project implements a **Predictive Risk Model** designed to identify high-risk patients *before* discharge, quantifying not just clinical risk, but **Financial Exposure ($)**.

## 💼 Business Context (The "Why")
Under the **Hospital Readmissions Reduction Program (HRRP)**, Medicare reduces payments to hospitals with excess readmissions.
* **The Goal:** Reduce the 30-day readmission rate.
* **The Financial Impact:** Preventing just 5% of readmissions in high-cost diagnosis groups (e.g., Sepsis, Heart Failure) can save millions in non-reimbursable costs.

## 🛠️ Technical Solution
I built an end-to-end pipeline simulating a hospital environment:

1.  **Synthetic Data Generation (Python):** Created a HIPPA-compliant dataset of 15,000 patients using `numpy/pandas`.
    * *Variables:* LOS (Length of Stay), ICD-10 Diagnosis codes, Comorbidities (Diabetes, Hypertension), and Billing Data.
    * *Logic:* Modeled readmission probabilities based on age, prior visits, and chronic conditions.
2.  **Risk Modeling:** Calculated individual probability scores and financial penalty exposure per patient.
3.  **Actionable Dashboard (Power BI):**
    * **"Discharge Priority Queue":** A ranked list of patients with the highest financial risk for immediate Case Management intervention.
    * **Comorbidity Analysis:** Visualizing how Diabetes multiplies readmission risk.

## 📊 Key Insights (from Synthetic Data)
* **The "Sepsis" Factor:** While Sepsis patients represent a smaller volume, they account for disproportionately high financial risk due to long LOS and high readmission probability.
* **Diabetes Multiplier:** Patients with Diabetes showed a **3x higher readmission rate** compared to non-diabetics, suggesting the need for specialized endocrine discharge planning.
* **Total Exposure:** Identifyied **$5M** in potential financial penalties in the current cohort.

## ⚙️ How to Run
1.  Run the Python script to generate the dataset:
    ```bash
    python generate_hospital_data.py
    ```
2.  Open the Power BI file (`Healthcare_Readmission.pbix`) and refresh data.

---
### Author
**Glauber Rocha**
*Data Analytics & Finance Specialist*
