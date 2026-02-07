# 📈 Hotel Revenue Management & Occupancy Forecasting

## 📌 Project Overview
Maximizing **RevPAR** (Revenue Per Available Room) requires selling the right room to the right customer at the right price. This project builds a forecasting engine that predicts future occupancy (90 days out) and suggests dynamic pricing adjustments.

## 💼 Business Problem
- **Issue:** Static pricing leaves money on the table during high demand and fails to attract guests during low demand.
- **Goal:** Forecast occupancy rates and automate ADR (Average Daily Rate) recommendations.
- **Impact:** Increase overall revenue through Yield Management strategies.

## 🛠️ Tech Stack
- **Language:** Python
- **Libraries:** Pandas, Scikit-Learn (Random Forest Regressor).
- **Visualization:** Power BI (Forecast vs. History Line Charts).

## 📊 Methodology
1. **Time Series Simulation:** Generated 2 years of historical daily data with seasonality, weekends, and event spikes.
2. **Feature Engineering:** Extracted temporal features (Day of Week, Month, Holiday Flags) to train the regressor.
3. **Forecasting:** Predicted occupancy for the next 3 months.
4. **Dynamic Pricing Logic:** Implemented a rule-based algorithm to surge prices when predicted occupancy > 85%.

## 📈 Key Results
- **Accurate Forecasting:** The model captures weekly seasonality and peak seasons.
- **Strategic Pricing:** The dashboard highlights days where ADR should be increased, directly boosting projected RevPAR.

## 🚀 How to Run
1. Run the script: `python project_revenue_management.py`
2. The script will generate `revenue_forecast_powerbi.csv`.
3. Use Power BI to visualize the "Forecast vs History" trend line.
