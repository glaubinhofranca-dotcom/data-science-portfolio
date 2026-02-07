# ⚙️ Hotel Predictive Maintenance Analytics

## 📌 Project Overview
Equipment failure (HVAC, Elevators, Boilers) ruins the guest experience and increases costs. This project applies Predictive Analytics to IoT sensor data to forecast equipment failures before they happen.

## 💼 Business Problem
- **Issue:** Reactive maintenance leads to downtime, guest complaints, and high emergency repair costs.
- **Goal:** Transition from Reactive to Predictive maintenance using risk scores.
- **Impact:** Reduced downtime and optimized maintenance scheduling.

## 🛠️ Tech Stack
- **Language:** Python
- **Libraries:** Pandas, Scikit-Learn (Random Forest Classifier), NumPy.
- **Visualization:** Power BI (Risk Ranking Dashboard).

## 📊 Methodology
1. **IoT Data Simulation:** Generated sensor readings (Temperature, Vibration) and maintenance logs for 200+ assets.
2. **Feature Engineering:** Calculated "Days Since Last Maintenance" and "Age of Equipment".
3. **Modeling:** Trained a **Random Forest** model to predict the probability of failure (`Will_Fail`).
4. **Risk Classification:** Categorized assets into High, Medium, and Low risk for prioritization.

## 📈 Key Results
- **Risk Identification:** The model successfully flagged equipment with abnormal vibration and temperature patterns.
- **Operational Dashboard:** Provides a prioritized "Inspect Immediately" list for the engineering team.

## 🚀 How to Run
1. Run the script: `python main_project.py`.
2. The script will generate `final_predictions_powerbi.csv` and `feature_importance.csv`.
3. Import into Power BI to visualize the Asset Health & Risk Matrix.
