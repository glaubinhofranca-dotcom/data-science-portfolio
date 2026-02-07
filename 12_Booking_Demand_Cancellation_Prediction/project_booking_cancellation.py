import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, roc_auc_score

# ==========================================
# CONFIGURATION
# ==========================================
np.random.seed(101)  # Fixed seed for reproducibility
OUTPUT_DIR = "outputs_booking"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

print(">>> Starting Project 1: Hotel Booking Cancellation Prediction...")

# ==========================================
# 1. SYNTHETIC DATA GENERATION
# ==========================================
print(f"[{datetime.now().strftime('%H:%M:%S')}] Generating synthetic bookings...")

n_rows = 5000
current_date = datetime(2025, 6, 1)

# Simulating data distributions
market_segments = ['Online TA', 'Offline TA/TO', 'Corporate', 'Direct', 'Groups']
deposit_types = ['No Deposit', 'Non Refundable', 'Refundable']
customer_types = ['Transient', 'Transient-Party', 'Contract', 'Group']
room_types = ['A', 'D', 'E', 'F', 'G'] # A=Standard, G=Suite

data = {
    'Booking_ID': [f"BK_{i:04d}" for i in range(n_rows)],
    'Lead_Time': np.random.gamma(shape=2, scale=30, size=n_rows).astype(int), # Skewed distribution
    'Arrival_Date': [current_date + timedelta(days=np.random.randint(0, 180)) for _ in range(n_rows)],
    'Stay_Nights': np.random.poisson(lam=3, size=n_rows) + 1, # Min 1 night
    'Adults': np.random.choice([1, 2, 3], size=n_rows, p=[0.25, 0.70, 0.05]),
    'Children': np.random.choice([0, 1, 2], size=n_rows, p=[0.9, 0.07, 0.03]),
    'Market_Segment': np.random.choice(market_segments, size=n_rows, p=[0.45, 0.20, 0.10, 0.15, 0.10]),
    'Distribution_Channel': 'TA/TO', # Simplified for this example
    'Is_Repeated_Guest': np.random.choice([0, 1], size=n_rows, p=[0.90, 0.10]),
    'Previous_Cancellations': np.random.choice([0, 1, 2], size=n_rows, p=[0.95, 0.04, 0.01]),
    'Deposit_Type': np.random.choice(deposit_types, size=n_rows, p=[0.85, 0.14, 0.01]),
    'ADR': np.random.normal(120, 35, n_rows).round(2), # Average Daily Rate ($)
    'Required_Car_Parking_Spaces': np.random.choice([0, 1], size=n_rows, p=[0.90, 0.10]),
    'Total_Of_Special_Requests': np.random.randint(0, 4, size=n_rows)
}

df = pd.DataFrame(data)

# Logic to determine "Is_Canceled" (Target) based on behavior
# Rule 1: High Lead Time (> 90 days) increases cancellation risk
# Rule 2: "Non Refundable" deposit decreases risk significantly
# Rule 3: Previous history of cancellation increases risk
def simulate_cancellation(row):
    prob = 0.20 # Base rate
    
    if row['Lead_Time'] > 90: prob += 0.30
    if row['Lead_Time'] < 3: prob -= 0.10
    if row['Deposit_Type'] == 'Non Refundable': prob -= 0.40 # Strong commitment
    if row['Market_Segment'] == 'Groups': prob += 0.15
    if row['Is_Repeated_Guest'] == 1: prob -= 0.10
    if row['Previous_Cancellations'] > 0: prob += 0.20
    if row['Total_Of_Special_Requests'] > 0: prob -= 0.05 # Engaged customer
    
    # Clip probability between 0 and 1
    prob = max(0, min(1, prob))
    return 1 if np.random.rand() < prob else 0

df['Is_Canceled'] = df.apply(simulate_cancellation, axis=1)

# Feature Engineering: Total Booking Value
df['Total_Revenue_Potential'] = df['ADR'] * df['Stay_Nights']

print(f"Data generated. Cancellation Rate: {df['Is_Canceled'].mean():.2%}")
df.to_csv(f"{OUTPUT_DIR}/raw_hotel_bookings.csv", index=False)

# ==========================================
# 2. MODEL TRAINING
# ==========================================
print(f"[{datetime.now().strftime('%H:%M:%S')}] Training prediction model...")

# Encoding Categorical Variables
le = LabelEncoder()
cat_cols = ['Market_Segment', 'Deposit_Type']
for col in cat_cols:
    df[f"{col}_Code"] = le.fit_transform(df[col])

features = ['Lead_Time', 'Stay_Nights', 'ADR', 'Total_Of_Special_Requests', 
            'Previous_Cancellations', 'Is_Repeated_Guest', 
            'Market_Segment_Code', 'Deposit_Type_Code']

X = df[features]
y = df['Is_Canceled']

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Model: Random Forest
rf = RandomForestClassifier(n_estimators=150, max_depth=10, random_state=42)
rf.fit(X_train, y_train)

# Metrics
y_pred = rf.predict(X_test)
roc = roc_auc_score(y_test, rf.predict_proba(X_test)[:, 1])
print("\n--- Model Performance ---")
print(classification_report(y_test, y_pred))
print(f"ROC-AUC Score: {roc:.3f}")

# Feature Importance
feat_imp = pd.DataFrame({'Feature': features, 'Importance': rf.feature_importances_})
feat_imp = feat_imp.sort_values('Importance', ascending=False)
feat_imp.to_csv(f"{OUTPUT_DIR}/booking_feature_importance.csv", index=False)

# ==========================================
# 3. EXPORT FOR POWER BI
# ==========================================
print(f"[{datetime.now().strftime('%H:%M:%S')}] Exporting final dataset...")

# Apply model to ALL data to simulate production dashboard
df['Cancel_Probability'] = rf.predict_proba(X)[:, 1]

# Business Logic: Classify Risk
df['Risk_Category'] = np.where(df['Cancel_Probability'] > 0.7, 'High Risk',
                      np.where(df['Cancel_Probability'] > 0.4, 'Medium Risk', 'Low Risk'))

# Business Logic: Calculate Revenue at Risk
# If probability is high, we consider that revenue "at risk"
df['Revenue_at_Risk'] = df['Total_Revenue_Potential'] * df['Cancel_Probability']

# Save final file
df.to_csv(f"{OUTPUT_DIR}/hotel_bookings_powerbi.csv", index=False)

print(f"\n>>> DONE! Files saved in '{OUTPUT_DIR}'.")
print(">>> Key file for Power BI: 'hotel_bookings_powerbi.csv'")