# 📦 Supply Chain Control Tower: Inventory Optimization & Risk Analysis

![Python](https://img.shields.io/badge/Python-ABC%20Analysis-blue)
![Power BI](https://img.shields.io/badge/PowerBI-Control%20Tower-yellow)
![Domain](https://img.shields.io/badge/Industry-Logistics%20%26%20Retail-orange)

## 📋 Executive Summary
In retail and logistics, stockouts in high-demand products kill revenue, while overstock kills cash flow.

This project builds a **Supply Chain Control Tower** that automates **ABC Analysis** (Pareto Principle) to identify critical inventory risks. It processes 5,000 SKUs to flag items where "Revenue at Risk" exceeds acceptable thresholds.

## 💼 Business Problem
* **Stockouts:** Losing sales on "Class A" products (Top 80% revenue drivers).
* **Overstock:** Freezing capital in slow-moving "Class C" inventory.
* **Goal:** Optimize the **Reorder Point (ROP)** and **Safety Stock** levels to balance service level vs. holding costs.

## 🛠️ Technical Solution
1.  **Inventory Engineering (Python):**
    * **ABC Classification:** Segmented SKUs based on cumulative revenue impact (Pareto 80/20 rule).
    * **Safety Stock Calculation:** Used statistical demand volatility (Z-Score 1.65 for 95% Service Level) and Lead Time variability to calculate optimal buffers.
    * **Stock Status Logic:** flagged items as "Critical Low" (below ROP) or "Overstock" (excessive coverage).
2.  **Control Tower Dashboard (Power BI):**
    * **Revenue at Risk KPI:** Quantifies the potential sales loss ($690M) from current stockouts.
    * **Action List:** A prioritized table of Class A items needing immediate replenishment.

## 📊 Key Insights
* **The "Class A" Crisis:** While Class A items make up the minority of SKUs, they account for **70% of the Revenue at Risk**. Immediate procurement focus is required here.
* **Efficiency Gap:** 20% of the inventory value is tied up in "Overstock", representing capital that could be redeployed.
* **Operational Risk:** 502 SKUs are critically low, threatening a potential **$690M** loss in annual turnover if not replenished.

## ⚙️ How to Run
1.  Generate the dataset:
    ```bash
    python generate_supply_chain_data.py
    ```
2.  Open `Supply_Chain_Analytics.pbix` in Power BI.

---
### Author
**Glauber Rocha**
*Operations & Analytics Specialist*
