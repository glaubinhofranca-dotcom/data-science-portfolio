import pandas as pd
import numpy as np
import os
from datetime import datetime
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# ==========================================
# CONFIGURATION
# ==========================================
np.random.seed(42)
OUTPUT_DIR = "outputs_segmentation"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

print(">>> Starting Project 3: Guest Segmentation (Clustering)...")

# ==========================================
# 1. GENERATE SYNTHETIC GUEST DATA
# ==========================================
print(f"[{datetime.now().strftime('%H:%M:%S')}] Generating guest profiles...")

n_guests = 2000

# We will create clear patterns to ensure clustering works beautifully
# Group 1: Budget Travelers (Low ADR, Low Lead Time, Low Special Requests)
# Group 2: VIP / Luxury (High ADR, High Special Requests, Long Stays)
# Group 3: Corporate (Mid ADR, Very Short Lead Time, Weekdays)
# Group 4: Families (Mid ADR, Long Lead Time, High Special Requests)

data = []

for i in range(n_guests):
    # Randomly assign a "hidden" profile to generate features
    profile = np.random.choice(['Budget', 'VIP', 'Corporate', 'Family'], p=[0.4, 0.1, 0.2, 0.3])
    
    guest_id = f"GST_{i+1:04d}"
    
    if profile == 'Budget':
        adr = np.random.normal(80, 15)
        stays = np.random.randint(1, 3)
        lead_time = np.random.randint(1, 30)
        requests = 0
        age = np.random.randint(18, 30)
    
    elif profile == 'VIP':
        adr = np.random.normal(350, 50)
        stays = np.random.randint(3, 10)
        lead_time = np.random.randint(15, 60)
        requests = np.random.randint(2, 6)
        age = np.random.randint(35, 60)
        
    elif profile == 'Corporate':
        adr = np.random.normal(150, 20)
        stays = np.random.randint(1, 4)
        lead_time = np.random.randint(1, 14) # Last minute
        requests = np.random.choice([0, 1])
        age = np.random.randint(25, 50)
        
    elif profile == 'Family':
        adr = np.random.normal(200, 30)
        stays = np.random.randint(4, 14)
        lead_time = np.random.randint(60, 180) # Plans ahead
        requests = np.random.randint(1, 4)
        age = np.random.randint(30, 50)
    
    # Add some noise/randomness so it's not perfect
    row = {
        'Guest_ID': guest_id,
        'Age': age,
        'Avg_Daily_Rate': round(max(50, adr + np.random.normal(0, 10)), 2),
        'Total_Stays': max(1, stays),
        'Avg_Lead_Time': max(0, int(lead_time + np.random.normal(0, 5))),
        'Total_Special_Requests': max(0, requests)
    }
    data.append(row)

df = pd.DataFrame(data)
df.to_csv(f"{OUTPUT_DIR}/raw_guests.csv", index=False)

# ==========================================
# 2. DATA PREPROCESSING & K-MEANS
# ==========================================
print(f"[{datetime.now().strftime('%H:%M:%S')}] Running K-Means Clustering...")

# Features to use for clustering
features = ['Avg_Daily_Rate', 'Total_Stays', 'Avg_Lead_Time', 'Total_Special_Requests']

# Scaling is CRITICAL for K-Means (StandardScaler z-score)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df[features])

# Train K-Means with 4 clusters
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
clusters = kmeans.fit_predict(X_scaled)

df['Cluster_ID'] = clusters

# Evaluate Quality
score = silhouette_score(X_scaled, clusters)
print(f"Clustering Silhouette Score: {score:.2f} (Close to 1 is perfect)")

# ==========================================
# 3. INTERPRETATION & NAMING
# ==========================================
print(f"[{datetime.now().strftime('%H:%M:%S')}] Naming the clusters...")

# Calculate mean values per cluster to understand what they are
summary = df.groupby('Cluster_ID')[features].mean()
print("\nCluster Summary (Means):")
print(summary)

# Logic to Auto-Name Clusters for Power BI
# We look at the summary and assign names based on rules
cluster_names = {}
for cluster_id, row in summary.iterrows():
    name = "Standard Guest" # Default
    
    # Rules based on the means we generated
    if row['Avg_Daily_Rate'] > 250:
        name = "VIP / Luxury"
    elif row['Avg_Daily_Rate'] < 100 and row['Avg_Lead_Time'] < 40:
        name = "Budget Traveler"
    elif row['Avg_Lead_Time'] > 50 and row['Total_Stays'] > 3:
        name = "Family / Planner"
    elif row['Avg_Lead_Time'] < 20 and row['Total_Stays'] < 4:
        name = "Corporate / Short Stay"
        
    cluster_names[cluster_id] = name

df['Segment_Name'] = df['Cluster_ID'].map(cluster_names)

# Save Final File
df.to_csv(f"{OUTPUT_DIR}/guest_segmentation_powerbi.csv", index=False)

print(f"\n>>> DONE! Files saved in '{OUTPUT_DIR}'.")
print(">>> Import 'guest_segmentation_powerbi.csv' into Power BI.")