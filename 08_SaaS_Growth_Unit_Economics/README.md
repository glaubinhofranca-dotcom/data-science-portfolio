# 🚀 SaaS Growth Analytics: Unit Economics & Churn Prediction

![Python](https://img.shields.io/badge/Python-Cohort%20Analysis-blue)
![Power BI](https://img.shields.io/badge/PowerBI-Growth%20Dashboard-pink)
![Industry](https://img.shields.io/badge/Industry-Tech%20%26%20Startups-purple)

## 📋 Executive Summary
In the Subscription Economy (SaaS), revenue is recurring, but so is the risk of losing customers.

This project focuses on **Unit Economics**—analyzing the profitability of a customer on a per-unit basis. Using a synthetic dataset of 8,000 subscribers, I built a dashboard to track **MRR**, **LTV**, and **Churn**, helping Product Managers identify high-value segments.

## 💼 Business Metrics
* **MRR (Monthly Recurring Revenue):** The predictability of the revenue stream.
* **Churn Rate:** The percentage of subscribers who cancel their recurring service.
* **LTV (Lifetime Value):** The total revenue expected from a single customer over their lifespan.

## 🛠️ Technical Solution
1.  **Data Simulation (Python):**
    * Modeled subscription lifecycles with realistic churn probabilities based on segments (SMB vs. Enterprise).
    * Calculated **LTV** dynamically based on retention months and pricing tiers.
2.  **Growth Dashboard (Power BI):**
    * **Segment Analysis:** Visualized how "Enterprise" clients drive 60%+ of revenue despite being only 10% of the volume.
    * **Channel ROI:** Identified "Referral" as the acquisition channel with the highest LTV, suggesting a shift in marketing spend.

## 📊 Key Insights
* **The "Whale" Strategy:** Enterprise customers showed a **50x higher LTV** compared to SMBs, validating a sales-led growth strategy over product-led growth for revenue maximization.
* **Churn Alert:** "Paid Ads" acquisition channel showed the highest Churn Rate, indicating low-quality leads compared to Organic/Referral.

## ⚙️ How to Run
1.  Generate the data:
    ```bash
    python generate_saas_data.py
    ```
2.  Open `SaaS_Growth_Analytics.pbix` in Power BI.

---
### Author
**Glauber Rocha**
*Product Data Analyst*
