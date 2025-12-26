import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.metrics import classification_report, confusion_matrix, precision_recall_curve, auc
from sklearn.preprocessing import StandardScaler

# ==========================================
# CONFIGURATION
# ==========================================
np.random.seed(42)
OUTPUT_DIR = "outputs_finance_fraud"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

print(">>> Starting Finance Project 2: Credit Card Fraud Detection...")

# ==========================================
# 1. GENERATE SYNTHETIC TRANSACTION DATA
# ==========================================
print(f"[{datetime.now().strftime('%H:%M:%S')}] Generating 50,000 transactions (Imbalanced)...")

n_transactions = 50000
fraud_rate = 0.005  # 0.5% fraud rate (Very realistic)

# Simulate Time (Seconds since midnight)
# Legitimate transactions happen mostly during day, Frauds spread out or late night
time_data = np.random.randint(0, 86400, n_transactions)

# Simulate Amount (Log-normal distribution)
# Most transactions are small ($10-$100), outliers are huge
amount_data = np.random.lognormal(mean=3.5, sigma=1.0, size=n_transactions)

# Simulate "Anonymized Features" (V1, V2...) typically found in bank datasets (PCA components)
# We generate random noise
V1 = np.random.normal(0, 1, n_transactions)
V2 = np.random.normal(0, 1, n_transactions)
V3 = np.random.normal(0, 1, n_transactions)

df = pd.DataFrame({
    'Transaction_ID': [f"TRX_{i+1:06d}" for i in range(n_transactions)],
    'Time_Seconds': time_data,
    'Amount': amount_data.round(2),
    'V1': V1, 'V2': V2, 'V3': V3
})

# INJECT FRAUD LOGIC
# Fraudsters tend to make:
# 1. Very high amounts OR very small testing amounts
# 2. Transactions at weird times (3 AM)
# 3. Specific patterns in V features (simulating card operational data)

def inject_fraud(row):
    # Base probability
    prob = 0.0
    
    # Rule 1: High Amount Anomaly
    if row['Amount'] > 500: prob += 0.3
    
    # Rule 2: Late night (00:00 to 05:00)
    if row['Time_Seconds'] < 18000: prob += 0.2
    
    # Rule 3: Specific "V" pattern (simulating geo-location mismatch)
    if row['V1'] < -2: prob += 0.4
    
    # Inject randomly based on calculated risk, but keep total rate low
    is_fraud = 1 if (np.random.rand() < prob) and (np.random.rand() < 0.05) else 0
    return is_fraud

df['Class'] = df.apply(inject_fraud, axis=1)

print(f"Total Transactions: {n_transactions}")
print(f"Total Frauds: {df['Class'].sum()} ({df['Class'].mean():.2%})")

# ==========================================
# 2. MODELING (Handling Imbalance)
# ==========================================
print(f"[{datetime.now().strftime('%H:%M:%S')}] Training Fraud Detection Models...")

# Features
X = df[['Time_Seconds', 'Amount', 'V1', 'V2', 'V3']]
y = df['Class']

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

# MODEL 1: Isolation Forest (Unsupervised Anomaly Detection)
# Great for finding "new" fraud patterns we haven't seen before
iso_forest = IsolationForest(contamination=fraud_rate, random_state=42)
iso_forest.fit(X_train)
# Isolation Forest predicts -1 for anomaly, 1 for normal. We map -1 to 1 (Fraud)
y_pred_iso = iso_forest.predict(X_test)
y_pred_iso = [1 if x == -1 else 0 for x in y_pred_iso]

# MODEL 2: Random Forest with Class Weighting (Supervised)
# 'class_weight="balanced"' penalizes mistakes on the minority class more
rf = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)
y_proba_rf = rf.predict_proba(X_test)[:, 1]

# ==========================================
# 3. EVALUATION (Precision-Recall is King)
# ==========================================
print("\n--- Random Forest Performance (Supervised) ---")
print(classification_report(y_test, y_pred_rf))

# Calculate Precision-Recall AUC (Better than ROC for imbalance)
precision, recall, _ = precision_recall_curve(y_test, y_proba_rf)
pr_auc = auc(recall, precision)
print(f"PR-AUC Score: {pr_auc:.3f}")

# Confusion Matrix to show savings
tn, fp, fn, tp = confusion_matrix(y_test, y_pred_rf).ravel()
print(f"Detected Frauds (TP): {tp}")
print(f"Missed Frauds (FN): {fn} (Risk of Loss)")
print(f"False Alarms (FP): {fp} (Customer Friction)")

# ==========================================
# 4. EXPORT FOR DASHBOARD
# ==========================================
print(f"[{datetime.now().strftime('%H:%M:%S')}] Exporting data for Power BI...")

# Run model on full dataset for visualization
df['Fraud_Probability'] = rf.predict_proba(X)[:, 1]
df['Predicted_Class'] = np.where(df['Fraud_Probability'] > 0.5, 'Fraud Alert', 'Legitimate')

# Logic: Flag High-Risk for manual review
# If probability is 0.3 to 0.5, it's "Suspicious"
df['Status'] = np.where(df['Fraud_Probability'] > 0.8, 'Auto-Block',
               np.where(df['Fraud_Probability'] > 0.4, 'Manual Review', 'Approved'))

# Calculate "Saved Money" (Assuming we blocked the frauds)
df['Potential_Loss_Saved'] = np.where((df['Class']==1) & (df['Status']!='Approved'), df['Amount'], 0)

df.to_csv(f"{OUTPUT_DIR}/fraud_detection_powerbi.csv", index=False)
print(f"\n>>> DONE! Files saved in '{OUTPUT_DIR}'.")