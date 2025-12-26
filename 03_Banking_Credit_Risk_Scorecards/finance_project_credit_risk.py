import pandas as pd
import numpy as np
import os
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, roc_auc_score, roc_curve

# ==========================================
# CONFIGURATION
# ==========================================
np.random.seed(42)
OUTPUT_DIR = "outputs_finance_risk"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

print(">>> Starting Finance Project 1: Credit Risk Scoring Model...")

# ==========================================
# 1. GENERATE SYNTHETIC BANKING DATA
# ==========================================
print(f"[{datetime.now().strftime('%H:%M:%S')}] Generating loan application data...")

n_clients = 10000

# Generating base features
data = {
    'Client_ID': [f"CL_{i+1:05d}" for i in range(n_clients)],
    'Age': np.random.randint(21, 75, n_clients),
    'Annual_Income': np.random.lognormal(mean=10.5, sigma=0.6, size=n_clients).round(-2), # Lognormal is realistic for income
    'Years_Employed': np.random.randint(0, 20, n_clients),
    'Home_Ownership': np.random.choice(['RENT', 'MORTGAGE', 'OWN'], n_clients, p=[0.4, 0.4, 0.2]),
    'Loan_Amount': np.random.randint(1000, 35000, n_clients),
    'Loan_Purpose': np.random.choice(['EDUCATION', 'MEDICAL', 'VENTURE', 'PERSONAL', 'DEBT_CONSOLIDATION'], n_clients),
    'Interest_Rate': np.random.uniform(5.0, 20.0, n_clients).round(2),
    'Credit_History_Length_Years': np.random.randint(1, 30, n_clients),
    'Previous_Defaults': np.random.choice([0, 1], n_clients, p=[0.85, 0.15]) # 15% had a default before
}

df = pd.DataFrame(data)

# Feature Engineering: Debt-to-Income Ratio (DTI) - CRITICAL for Finance
# Calculating monthly income vs monthly loan payment (simplified)
df['Monthly_Income'] = df['Annual_Income'] / 12
df['Estimated_Monthly_Payment'] = (df['Loan_Amount'] * (1 + (df['Interest_Rate']/100))) / 24 # Assuming 2 year loan
df['DTI_Ratio'] = df['Estimated_Monthly_Payment'] / df['Monthly_Income']

# Logic to Simulate TARGET (Default = 1)
# High DTI, Previous Defaults, Low Income, Renting -> Higher Risk
def simulate_default(row):
    score = 0
    if row['Previous_Defaults'] == 1: score += 2.5
    if row['DTI_Ratio'] > 0.40: score += 2.0  # High debt burden
    if row['Home_Ownership'] == 'RENT': score += 0.5
    if row['Years_Employed'] < 2: score += 1.0
    if row['Age'] < 25: score += 0.5
    if row['Annual_Income'] < 30000: score += 1.0
    
    # Sigmoid-like probability
    prob = 1 / (1 + np.exp(-(score - 3))) # Shift to adjust default rate
    return 1 if np.random.rand() < prob else 0

df['Default_On_File'] = df.apply(simulate_default, axis=1)

print(f"Default Rate in Dataset: {df['Default_On_File'].mean():.2%}")
df.to_csv(f"{OUTPUT_DIR}/raw_loan_data.csv", index=False)

# ==========================================
# 2. TRAIN SCORING MODEL (Logistic Regression)
# ==========================================
print(f"[{datetime.now().strftime('%H:%M:%S')}] Training Credit Scorecard...")

# Define Predictors
numeric_features = ['Age', 'Annual_Income', 'Years_Employed', 'Loan_Amount', 'Interest_Rate', 'DTI_Ratio', 'Credit_History_Length_Years']
categorical_features = ['Home_Ownership', 'Loan_Purpose', 'Previous_Defaults'] # Treating prev_default as categorical

X = df[numeric_features + categorical_features]
y = df['Default_On_File']

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Pipeline: Preprocessing + Model
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])

# Logistic Regression is standard for Scorecards (Interpretable)
clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('classifier', LogisticRegression(class_weight='balanced', random_state=42))])

clf.fit(X_train, y_train)

# Metrics
y_pred_proba = clf.predict_proba(X_test)[:, 1]
roc = roc_auc_score(y_test, y_pred_proba)
print("\n--- Model Performance ---")
print(f"ROC-AUC Score: {roc:.3f} (Industry standard > 0.7)")

# ==========================================
# 3. CREATE CREDIT SCORE (SCALING)
# ==========================================
print(f"[{datetime.now().strftime('%H:%M:%S')}] Calculating Credit Scores (300-850)...")

# Apply model to full dataset
df['PD'] = clf.predict_proba(X)[:, 1] # Probability of Default

# Scaling Logic: Convert PD to a Score (like FICO)
# Formula: Score = Offset - (Factor * ln(Odds))
# Simplified mapping: Low PD -> High Score (850), High PD -> Low Score (300)
min_score = 300
max_score = 850

# Invert probability (Probability of Paying)
df['Prob_Non_Default'] = 1 - df['PD']

# Linear mapping for simplicity in this demo (In real life, we use Log Odds)
df['Credit_Score'] = min_score + (df['Prob_Non_Default'] * (max_score - min_score))
df['Credit_Score'] = df['Credit_Score'].astype(int)

# Create Tiers
df['Risk_Rating'] = pd.cut(df['Credit_Score'], 
                           bins=[0, 579, 669, 739, 799, 900], 
                           labels=['Poor', 'Fair', 'Good', 'Very Good', 'Exceptional'])

# Decision Engine: Approve/Reject based on Cut-off
# Aggressive Strategy: Approve if Score > 600
df['Decision'] = np.where(df['Credit_Score'] >= 600, 'Approve', 'Reject')

# Finance Metrics: Expected Loss (EL)
# EL = PD * LGD * EAD
# LGD (Loss Given Default): Assume we lose 60% of value if they default
# EAD (Exposure at Default): The Loan Amount
df['LGD'] = 0.60 
df['EAD'] = df['Loan_Amount']
df['Expected_Loss'] = df['PD'] * df['LGD'] * df['EAD']

# Export for Power BI
cols_export = ['Client_ID', 'Annual_Income', 'Loan_Amount', 'Loan_Purpose', 
               'DTI_Ratio', 'Default_On_File', 'PD', 'Credit_Score', 
               'Risk_Rating', 'Decision', 'Expected_Loss']

df[cols_export].to_csv(f"{OUTPUT_DIR}/credit_risk_powerbi.csv", index=False)

print(f"\n>>> DONE! Files saved in '{OUTPUT_DIR}'.")
print(">>> Import 'credit_risk_powerbi.csv' into Power BI.")