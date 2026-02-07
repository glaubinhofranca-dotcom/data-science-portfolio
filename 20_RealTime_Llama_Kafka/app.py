import streamlit as st
import json
from kafka import KafkaConsumer
from llama_cpp import Llama
import time
import os

# --- Page Config ---
st.set_page_config(
    page_title="Real-Time AI Sentiment Trader",
    page_icon="⚡",
    layout="wide"
)

# --- Header ---
st.title("⚡ Real-Time Crypto Sentiment (Llama-3 + Kafka)")
st.markdown("Watching the `crypto_news` topic and analyzing market sentiment live.")

# --- 1. Load Model (Cached) ---
@st.cache_resource
def load_model():
    model_path = "finance_model_llama3.gguf"
    if not os.path.exists(model_path):
        st.error(f"❌ Model not found at {model_path}. Please move the file here!")
        return None
    
    print("🧠 Loading Llama-3... this might take a moment.")
    llm = Llama(
        model_path=model_path,
        n_ctx=512,        # Small context for speed
        n_threads=4,      # Use CPU cores
        verbose=False
    )
    return llm

llm = load_model()

# --- 2. AI Analysis Function ---
def analyze_sentiment(headline):
    prompt = f"""
    Instruction: Analyze the sentiment of this crypto news headline. 
    Classify strictly as: BULLISH, BEARISH, or NEUTRAL.
    
    Headline: "{headline}"
    
    Sentiment:"""
    
    output = llm(
        prompt, 
        max_tokens=10, # We only need one word
        stop=["\n"], 
        echo=False
    )
    return output['choices'][0]['text'].strip().upper()

# --- 3. Kafka Consumer Setup ---
# Initialize container elements for live updates
st.divider()
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📰 Live News Feed")
    news_placeholder = st.empty()

with col2:
    st.subheader("🤖 AI Verdict")
    verdict_placeholder = st.empty()

# Button to start the loop (Streamlit reruns the whole script on interaction)
start_btn = st.button("🔴 Start Live Feed")

if start_btn and llm:
    try:
        consumer = KafkaConsumer(
            'crypto_news',
            bootstrap_servers=['localhost:9092'],
            auto_offset_reset='latest',
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            consumer_timeout_ms=1000 # Don't block forever
        )
        
        st.toast("Connected to Kafka! Listening for news...", icon="📡")

        # History list to show scrolling feed
        history = []

        # Loop forever (until user stops or error)
        while True:
            for message in consumer:
                data = message.value
                headline = data['headline']
                timestamp = data['timestamp']
                
                # --- AI INFERENCE ---
                sentiment = analyze_sentiment(headline)
                
                # --- UPDATE UI ---
                # Add to history
                history.insert(0, {"time": timestamp, "news": headline, "sentiment": sentiment})
                history = history[:5] # Keep last 5
                
                # Render Feed
                with news_placeholder.container():
                    for item in history:
                        st.markdown(f"**{item['time']}**: {item['news']}")
                        st.divider()

                # Render Big Sentiment Badge
                with verdict_placeholder.container():
                    color = "gray"
                    if "BULLISH" in sentiment: color = "green"
                    if "BEARISH" in sentiment: color = "red"
                    
                    st.markdown(f"""
                        <div style="background-color:{color}; padding:20px; border-radius:10px; text-align:center;">
                            <h2 style="color:white; margin:0;">{sentiment}</h2>
                        </div>
                    """, unsafe_allow_html=True)
                
                # Force UI update sleep
                time.sleep(0.5)
                
    except Exception as e:
        st.error(f"Connection Error: {e}")