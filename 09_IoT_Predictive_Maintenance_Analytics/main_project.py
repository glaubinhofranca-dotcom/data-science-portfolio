import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.preprocessing import LabelEncoder

# Optional: Try to import XGBoost (just to show advanced capability in code)
try:
    import xgboost as xgb
    HAS_XGB = True
except ImportError:
    HAS_XGB = False

# ==========================================
# CONFIGURATION
# ==========================================
np.random.seed(42)
OUTPUT_DIR = "outputs"

# Create output folder if it doesn't exist
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

print(">>> Starting Hotel Predictive Maintenance Project...")

# ==========================================
# 1. SYNTHETIC DATASET GENERATION
# ==========================================
print(f"[{datetime.now().strftime('%H:%M:%S')}] Generating synthetic dataset...")

# Equipment list based on your specific hotel requirements
equipment_list = {
    "HVAC": 100, "Elevator": 2, "Laundry Machine": 4, "Dryer": 4,
    "Boiler": 3, "Pool Pump": 3, "Gas Generator": 1, "Grill": 2,
    "Pool Heater": 1, "Room HVAC": 2, "Pool Room HVAC": 1,
    "Fire Pit": 1, "EV Charger": 2, "Automatic Door": 2,
    "Electronic Locker": 120
}

data = []
# Set a reference date for the project (Simulation Date)
current_date = datetime(2025, 5, 1)

for eq_type, count in equipment_list.items():
    for i in range(count):
        # Generate unique ID (e.g., HVAC_001)
        eq_id = f"{eq_type.upper().replace(' ', '_')}_{i+1:03d}"
        
        # Simulate installation and maintenance dates
        install_date = current_date - timedelta(days=np.random.randint(100, 3000))
        last_maint = current_date - timedelta(days=np.random.randint(1, 365))
        
        # Calculate derived time metrics
        age_days = (current_date - install_date).days
        days_since_maint = (current_date - last_maint).days
        
        # Logic: Equipment is more likely to fail if old or not maintained recently
        base_fail_prob = 0.05
        if days_since_maint > 180: base_fail_prob += 0.2
        if age_days > 1500: base_fail_prob += 0.1
        if eq_type in ["Elevator", "Boiler"]: base_fail_prob += 0.1
        
        # Determine target variable (1 = Failure, 0 = No Failure)
        will_fail = 1 if np.random.rand() < base_fail_prob else 0
        
        # Simulate sensor readings 
        # (If failing, temperature and vibration are higher/unstable)
        temp = np.random.normal(70, 5) + (20 * will_fail * np.random.rand())
        vib = np.random.normal(0.5, 0.1) + (1.5 * will_fail * np.random.rand())
        
        row = {
            "Equipment_ID": eq_id,
            "Equipment_Type": eq_type,
            "Install_Date": install_date,
            "Last_Maintenance_Date": last_maint,
            "Usage_Hours": np.random.randint(500, 20000),
            "Number_of_Failures": np.random.choice([0, 1, 2, 3, 4], p=[0.6, 0.2, 0.1, 0.05, 0.05]),
            "Maintenance_Cost": round(np.random.uniform(100, 5000), 2),
            "Sensor_Temperature": round(temp, 1),
            "Sensor_Vibration": round(vib, 2),
            "Age_Days": age_days,
            "Days_Since_Maint": days_since_maint,
            "Will_Fail": will_fail  # Target variable
        }
        data.append(row)

df = pd.DataFrame(data)

# Save raw dataset (Optional, for record keeping)
df.to_csv(f"{OUTPUT_DIR}/hotel_maintenance_dataset.csv", index=False)
print(f"Dataset saved with {len(df)} equipment units.")

# ==========================================
# 2. EXPLORATORY DATA ANALYSIS (EDA)
# ==========================================
print(f"[{datetime.now().strftime('%H:%M:%S')}] Generating EDA charts...")

# KPI: Average Maintenance Cost by Type
cost_by_type = df.groupby("Equipment_Type")["Maintenance_Cost"].mean().sort_values()
plt.figure(figsize=(10, 6))
cost_by_type.plot(kind='barh', color='skyblue')
plt.title("Average Maintenance Cost by Equipment Type")
plt.xlabel("Cost ($)")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/eda_cost_by_type.png")
plt.close()

# KPI: Scatter Plot Vibration vs Temperature (Colored by Failure Status)
plt.figure(figsize=(8, 6))
sns.scatterplot(data=df, x="Sensor_Temperature", y="Sensor_Vibration", hue="Will_Fail", palette="coolwarm")
plt.title("Sensor Analysis: Temperature vs Vibration")
plt.savefig(f"{OUTPUT_DIR}/eda_sensors_scatter.png")
plt.close()

# ==========================================
# 3. MACHINE LEARNING MODELING
# ==========================================
print(f"[{datetime.now().strftime('%H:%M:%S')}] Training predictive model...")

# Data Preparation
le = LabelEncoder()
df['Type_Code'] = le.fit_transform(df['Equipment_Type'])

features = ['Type_Code', 'Usage_Hours', 'Number_of_Failures', 'Maintenance_Cost', 
            'Sensor_Temperature', 'Sensor_Vibration', 'Age_Days', 'Days_Since_Maint']

X = df[features]
y = df['Will_Fail']

# Split Data (70% Train, 30% Test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Model: Random Forest Classifier
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# Evaluation
y_pred = rf.predict(X_test)
roc = roc_auc_score(y_test, y_pred)
print("\n--- Model Results (Random Forest) ---")
print(classification_report(y_test, y_pred))
print(f"ROC-AUC Score: {roc:.2f}")

# Feature Importance Export (CORRECTED: Now exports with headers 'Feature' and 'Importance')
feature_df = pd.DataFrame({
    'Feature': features,
    'Importance': rf.feature_importances_
}).sort_values(by='Importance', ascending=False)

feature_df.to_csv(f"{OUTPUT_DIR}/feature_importance.csv", index=False)
print(f"Feature importance saved to '{OUTPUT_DIR}/feature_importance.csv'")

# ==========================================
# 4. FINAL EXPORT FOR POWER BI
# ==========================================
print(f"[{datetime.now().strftime('%H:%M:%S')}] Exporting final Power BI dataset...")

# Generate probabilities for the full dataset (Production Simulation)
df['Prob_Failure'] = rf.predict_proba(X)[:, 1]

# Create Risk Categories
df['Predicted_Risk'] = np.where(df['Prob_Failure'] > 0.6, "High Risk", 
                                np.where(df['Prob_Failure'] > 0.3, "Medium Risk", "Low Risk"))

# Suggest Action Plans
df['Action_Plan'] = np.where(df['Predicted_Risk'] == "High Risk", "Inspect Immediately",
                             np.where(df['Predicted_Risk'] == "Medium Risk", "Schedule Maintenance", "Monitor"))

# Save final enriched data
df.to_csv(f"{OUTPUT_DIR}/final_predictions_powerbi.csv", index=False)

print(f"\n>>> SUCCESS! All files are ready in the '{OUTPUT_DIR}' folder.")
print(">>> Next Step: Open Power BI and import 'final_predictions_powerbi.csv'.")