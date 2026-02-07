import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# ==========================================
# CONFIGURATION
# ==========================================
np.random.seed(42)
OUTPUT_DIR = "outputs_revenue"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

print(">>> Starting Project 2: Hotel Revenue Management & Forecasting...")

# ==========================================
# 1. GENERATE HISTORICAL DATA (2 Years)
# ==========================================
print(f"[{datetime.now().strftime('%H:%M:%S')}] Generating historical timeseries...")

# Date range: Past 2 years up to today
start_date = datetime(2023, 1, 1)
end_date = datetime(2025, 5, 30) # Let's assume 'today' is end of May 2025
date_range = pd.date_range(start=start_date, end=end_date, freq='D')
n_days = len(date_range)

df = pd.DataFrame({'Date': date_range})

# Feature Engineering: Extracting calendar patterns
df['Day_of_Week'] = df['Date'].dt.dayofweek # 0=Monday, 6=Sunday
df['Month'] = df['Date'].dt.month
df['Year'] = df['Date'].dt.year
df['Day_of_Year'] = df['Date'].dt.dayofyear
df['Is_Weekend'] = df['Day_of_Week'].apply(lambda x: 1 if x >= 5 else 0)

# Simulate Seasonality (Sine wave for yearly seasonality + random noise)
# Peak in Summer (Months 6-8) and Holidays (Dec)
seasonality = np.sin(2 * np.pi * df['Day_of_Year'] / 365)
base_occupancy = 0.60 # 60% base
weekend_boost = df['Is_Weekend'] * 0.25 # Weekends are 25% busier

# Add Events/Holidays logic (Random spikes)
events = np.random.choice([0, 0.15, 0.30], size=n_days, p=[0.95, 0.04, 0.01])
df['Event_Factor'] = events

# Calculate Final Occupancy (capped at 100% and min 10%)
raw_occupancy = base_occupancy + (seasonality * 0.15) + weekend_boost + events + np.random.normal(0, 0.05, n_days)
df['Occupancy_Rate'] = np.clip(raw_occupancy, 0.10, 1.00)

# Simulate ADR (Average Daily Rate) - Prices fluctuate with demand
# Base price $150 + premium for high occupancy days
df['Actual_ADR'] = 150 + (df['Occupancy_Rate'] * 100) + np.random.normal(0, 10, n_days)
df['RevPAR'] = df['Actual_ADR'] * df['Occupancy_Rate'] # Revenue Per Available Room

# Save historical data
df.to_csv(f"{OUTPUT_DIR}/historical_revenue_data.csv", index=False)

# ==========================================
# 2. TRAIN FORECASTING MODEL
# ==========================================
print(f"[{datetime.now().strftime('%H:%M:%S')}] Training forecasting model...")

# We want to predict 'Occupancy_Rate' based on calendar features
features = ['Day_of_Week', 'Month', 'Day_of_Year', 'Is_Weekend', 'Event_Factor']
target = 'Occupancy_Rate'

X = df[features]
y = df[target]

# Train (using all historical data to predict future)
# For a real project, we would do a time-series split, but here we train on all to forecast future
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# Evaluate on last 30 days just to print a metric
y_pred_hist = model.predict(X)
mae = mean_absolute_error(y, y_pred_hist)
print(f"Model Training MAE (Mean Absolute Error): {mae:.2%}")
# Insight: If MAE is 5%, it means our prediction is usually off by +/- 5% occupancy.

# ==========================================
# 3. FUTURE FORECAST & PRICING STRATEGY
# ==========================================
print(f"[{datetime.now().strftime('%H:%M:%S')}] Predicting next 90 days...")

# Create Future Dates (Next 90 days)
future_days = 90
future_start = end_date + timedelta(days=1)
future_range = pd.date_range(start=future_start, periods=future_days, freq='D')

future_df = pd.DataFrame({'Date': future_range})
future_df['Day_of_Week'] = future_df['Date'].dt.dayofweek
future_df['Month'] = future_df['Date'].dt.month
future_df['Year'] = future_df['Date'].dt.year
future_df['Day_of_Year'] = future_df['Date'].dt.dayofyear
future_df['Is_Weekend'] = future_df['Day_of_Week'].apply(lambda x: 1 if x >= 5 else 0)
# Assume random events for future (or input manual known events)
future_df['Event_Factor'] = np.random.choice([0, 0.15], size=future_days, p=[0.95, 0.05])

# Predict Occupancy
future_df['Predicted_Occupancy'] = model.predict(future_df[features])

# DYNAMIC PRICING LOGIC (The "Revenue Management" Brain)
# Rule: If demand is high, raise price. If low, lower price to attract volume.
base_rate = 150

def recommend_price(occupancy):
    if occupancy > 0.85:
        return base_rate * 1.40 # Surge pricing (+40%)
    elif occupancy > 0.60:
        return base_rate * 1.15 # Standard High (+15%)
    elif occupancy > 0.40:
        return base_rate * 1.00 # Base rate
    else:
        return base_rate * 0.85 # Discount (-15%)

future_df['Suggested_ADR'] = future_df['Predicted_Occupancy'].apply(recommend_price)

# Calculate Projected Revenue
future_df['Projected_RevPAR'] = future_df['Suggested_ADR'] * future_df['Predicted_Occupancy']
future_df['Data_Type'] = 'Forecast' # Label for Power BI

# Prepare Historical Data for Merge
df['Predicted_Occupancy'] = df['Occupancy_Rate'] # For history, predicted = actual
df['Suggested_ADR'] = df['Actual_ADR']
df['Projected_RevPAR'] = df['RevPAR']
df['Data_Type'] = 'History'

# Merge History + Forecast for Power BI
final_df = pd.concat([df, future_df], axis=0, ignore_index=True)

# Select clean columns
cols_to_export = ['Date', 'Day_of_Week', 'Is_Weekend', 'Data_Type', 
                  'Predicted_Occupancy', 'Suggested_ADR', 'Projected_RevPAR']

final_df[cols_to_export].to_csv(f"{OUTPUT_DIR}/revenue_forecast_powerbi.csv", index=False)

print(f"\n>>> DONE! Files saved in '{OUTPUT_DIR}'.")
print(">>> Import 'revenue_forecast_powerbi.csv' into Power BI.")