import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib # Para salvar o modelo em vez do h5

# --- Configuration ---
# Random Forest não precisa de "Sequências" temporais complexas como LSTM,
# ele olha o estado atual dos sensores. É mais simples e robusto.
NUM_ENGINES = 100
SENSORS = ['T24', 'T30', 'T50', 'P30', 'Nf', 'Nc', 'Ps30']

def generate_synthetic_data(num_engines=100):
    data = []
    print(f"🏭 Simulating telemetry for {num_engines} jet engines...")
    
    for engine_id in range(1, num_engines + 1):
        max_life = np.random.randint(150, 300)
        for cycle in range(1, max_life + 1):
            rul = max_life - cycle
            health = rul / max_life
            
            # Physics-based degradation + Noise
            noise = np.random.normal(0, 0.02, 7)
            s1 = 642 + (1 - health) * 20 + noise[0]
            s2 = 1588 + (1 - health) * 50 + noise[1]
            s3 = 1400 + (1 - health) * 70 + noise[2]
            s4 = 554 - (1 - health) * 30 + noise[3]
            s5 = 2388 + (1 - health) * 10 + noise[4]
            s6 = 9050 + (1 - health) * 100 + noise[5]
            s7 = 47 - (1 - health) * 5 + noise[6]
            
            data.append([engine_id, cycle, s1, s2, s3, s4, s5, s6, s7, rul])

    cols = ['id', 'cycle'] + SENSORS + ['RUL']
    return pd.DataFrame(data, columns=cols)

if __name__ == "__main__":
    # 1. Generate
    df = generate_synthetic_data(NUM_ENGINES)
    
    # 2. Train/Test
    X = df[SENSORS]
    y = df['RUL']
    
    print("🧠 Training Random Forest Regressor...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # 3. Save
    joblib.dump(model, "rf_engine_model.pkl")
    print("💾 Model saved as 'rf_engine_model.pkl'")