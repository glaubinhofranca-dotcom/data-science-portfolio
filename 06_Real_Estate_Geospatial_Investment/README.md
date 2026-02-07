# 🏠 PropTech: Real Estate Investment Opportunity Finder

![Python](https://img.shields.io/badge/Python-Geospatial-blue)
![Power BI](https://img.shields.io/badge/PowerBI-Map%20Analytics-yellow)
![Domain](https://img.shields.io/badge/Industry-Real%20Estate%20Investments-green)

## 📋 Executive Summary
In the competitive Boston Real Estate market, identifying undervalued properties with high rental yield potential requires analyzing thousands of listings instantly.

This project simulates an **Automated Investment Committee Tool** for a REIT (Real Estate Investment Trust). It ingests property data, calculates key financial metrics (**Cap Rate**, **ROI**), and visualizes "Buy" opportunities on an interactive geospatial dashboard.

## 💼 Business Problem
* **The Challenge:** Manual screening of property listings is slow and prone to bias.
* **The Goal:** Automatically flag properties that meet strict investment criteria:
    * **Cap Rate (Yield) > 5.5%** OR
    * **Projected ROI > 15%** (after renovation & resale).

## 🛠️ Technical Solution
1.  **Synthetic Market Data (Python):** Generated a realistic dataset of 2,000 properties across key Boston neighborhoods (Beacon Hill, Back Bay, Dorchester), modeling variables like:
    * *Fair Market Value vs. Listing Price* (identifying discounts).
    * *Renovation Costs* based on condition scores.
2.  **Financial Logic:** Implemented algorithms to calculate **Net Operating Income (NOI)** and **Capitalization Rates**.
3.  **Geospatial Dashboard (Power BI):**
    * **Value Hunting:** Scatter plots to find "Low Price / High ROI" outliers.
    * **Yield Mapping:** Geospatial analysis identifying which neighborhoods offer the best rental returns vs. capital appreciation.

## 📊 Key Insights
* **Yield vs. Prestige:** The analysis confirmed that while *Back Bay* commands higher prices, "up-and-coming" neighborhoods like *Dorchester* and *Fenway* offer significantly superior **Cap Rates (6%+)** for cash-flow focused investors.
* **The "Fixer-Upper" Strategy:** Properties with Condition Scores below 5, when renovated, showed the highest potential ROI (>20%) despite the upfront capital requirement.

## ⚙️ How to Run
1.  Run the generation script:
    ```bash
    python generate_real_estate_data.py
    ```
2.  Open `Real_Estate_Investment.pbix` in Power BI.

---
### Author
**Glauber Rocha**
*Asset Allocation & Analytics Specialist*
