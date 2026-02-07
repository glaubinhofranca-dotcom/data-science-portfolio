# ✈️ NASA Jet Engine: Predictive Maintenance Digital Twin

![Status](https://img.shields.io/badge/Status-Completed-success)
![Tech](https://img.shields.io/badge/Stack-RandomForest%20%7C%20Streamlit%20%7C%20Plotly-blue)
![Domain](https://img.shields.io/badge/Domain-Industrial%20IoT%20%7C%20Aerospace-orange)

## 📋 Executive Summary
Unscheduled downtime in aviation costs billions annually. Traditional maintenance is either **reactive** (fix when broken) or **preventive** (replace on schedule, wasting useful life).

This project implements a **Predictive Maintenance** system (Digital Twin) for Turbofan Jet Engines. By simulating sensor telemetry (Temperature, Pressure, Vibration) and applying a **Random Forest Regressor**, the system predicts the **Remaining Useful Life (RUL)** of an engine in real-time, allowing for "Just-in-Time" maintenance.

## 🏗️ Technical Architecture

1.  **Physics Simulation:**
    * Generates synthetic run-to-failure data based on NASA CMAPSS physics models.
    * Simulates degradation across 7 key sensors (Fan Speed, Core Speed, LPC/HPC Temperatures).

2.  **Machine Learning (Regression):**
    * **Model:** Random Forest Regressor (`scikit-learn`).
    * **Target:** Predict `RUL` (Remaining Useful Life) in cycles.
    * **Performance:** The model learns non-linear relationships between sensor noise and mechanical wear.

3.  **Real-Time Dashboard (Streamlit):**
    * Acts as a "Digital Twin" interface for engineers.
    * Visualizes the decay curve and alerts when RUL drops below safety thresholds.

## 🚀 How to Run

### 1. Train the AI Model
Generate data and train the predictive brain:

    python train_model.py

### 2. Launch the Digital Twin
Open the command center:

    streamlit run app.py

## 📊 Key Features
•	RUL Gauge: A visual countdown to engine failure.
•	Live Telemetry: Monitors T24, T30, P30, and Vibration sensors in real-time.
•	Alert System: Triggers "CRITICAL MAINTENANCE" warnings when RUL < 20 cycles.

## 📂 Project Structure
    22_NASA_Jet_Engine_Maintenance/
    ├── app.py                   # The Digital Twin Dashboard
    ├── train_model.py           # Data Generation & Model Training
    ├── rf_engine_model.pkl      # The Trained Brain (Random Forest)
    ├── requirements.txt         # Dependencies
    └── README.md                # Documentation

## 👨‍💻 Author
Glauber Rocha Senior Data Professional | AI Engineering