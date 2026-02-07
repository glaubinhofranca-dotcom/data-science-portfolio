import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
import time

# --- Page Config ---
st.set_page_config(layout="wide", page_title="NASA Digital Twin", page_icon="✈️")

st.markdown("""
<style>
    .stApp { background-color: #0E1117; }
</style>
""", unsafe_allow_html=True)

st.title("✈️ Jet Engine Digital Twin (Predictive Maintenance)")
st.markdown("Real-time telemetry analysis using **Random Forest AI** to predict Remaining Useful Life (RUL).")

# --- 1. Load Model ---
@st.cache_resource
def load_ai_brain():
    try:
        return joblib.load("rf_engine_model.pkl")
    except:
        return None

model = load_ai_brain()

if model is None:
    st.error("❌ Model not found! Please run 'train_model.py' first.")
    st.stop()

# --- 2. Simulation State ---
if 'cycle' not in st.session_state:
    st.session_state.cycle = 0
    st.session_state.health = 1.0
    st.session_state.history = []
    st.session_state.rul_prediction = 150

# --- 3. Sidebar ---
st.sidebar.header("⚙️ Simulation Controls")
reset_btn = st.sidebar.button("Reset Engine")

if reset_btn:
    st.session_state.cycle = 0
    st.session_state.health = 1.0
    st.session_state.history = []
    st.rerun()

# --- 4. Live Data Generation ---
def generate_live_reading(cycle, current_health):
    degradation = 0.0005 if cycle < 100 else 0.002
    new_health = max(0, current_health - degradation)
    noise = np.random.normal(0, 0.05, 7)
    
    readings = [
        642 + (1 - new_health) * 20 + noise[0],
        1588 + (1 - new_health) * 50 + noise[1],
        1400 + (1 - new_health) * 70 + noise[2],
        554 - (1 - new_health) * 30 + noise[3],
        2388 + (1 - new_health) * 10 + noise[4],
        9050 + (1 - new_health) * 100 + noise[5],
        47 - (1 - new_health) * 5 + noise[6]
    ]
    return readings, new_health

sensors, st.session_state.health = generate_live_reading(st.session_state.cycle, st.session_state.health)
st.session_state.cycle += 1
st.session_state.history.append(sensors)

# --- 5. AI Inference (Simpler for Random Forest) ---
# Random Forest only needs the current sensor values, not the history sequence
input_data = np.array(sensors).reshape(1, -1)
pred = model.predict(input_data)
st.session_state.rul_prediction = float(pred[0])

# --- 6. Dashboard Layout ---
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.markdown("### 📡 Telemetry")
    st.metric("Cycle Count", f"#{st.session_state.cycle}")
    st.metric("LPC Temperature (T24)", f"{sensors[0]:.1f} °R", delta=f"{(sensors[0]-642):.1f}")
    st.metric("HPC Pressure (P30)", f"{sensors[3]:.1f} psi", delta=f"{(sensors[3]-554):.1f}", delta_color="inverse")

with col2:
    st.markdown("### 🤖 AI Prediction (RUL)")
    rul = st.session_state.rul_prediction
    color = "green" if rul > 100 else "orange" if rul > 50 else "red"
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = rul,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Remaining Cycles"},
        gauge = {
            'axis': {'range': [0, 200]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 50], 'color': "rgba(255, 0, 0, 0.3)"},
                {'range': [50, 100], 'color': "rgba(255, 165, 0, 0.3)"}
            ],
            'threshold': {'line': {'color': "white", 'width': 4}, 'thickness': 0.75, 'value': rul}
        }
    ))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"})
    st.plotly_chart(fig, use_container_width=True)

with col3:
    st.markdown("### 📉 Vibration Analysis")
    chart_data = pd.DataFrame([x[5] for x in st.session_state.history], columns=["Vibration"])
    st.line_chart(chart_data, height=200)

if st.button("▶️ Run Simulation Step"):
    st.rerun()