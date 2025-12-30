import time
import json
import random
from kafka import KafkaProducer
from datetime import datetime

# --- Configuration ---
KAFKA_TOPIC = 'crypto_news'
KAFKA_SERVER = 'localhost:9092'

# --- Mock Data: Crypto Headlines ---
headlines = [
    "Bitcoin breaks $75k resistance level, analysts predict $100k soon.",
    "SEC announces strict regulations on DeFi protocols, market dips.",
    "Ethereum gas fees drop to record lows, usage spikes.",
    "Major exchange suffers security breach, 5000 BTC stolen.",
    "Federal Reserve hints at interest rate cuts, risk assets rally.",
    "New meme coin crashes 99% in 'rug pull' scam.",
    "Tesla resumes Bitcoin payments for electric vehicles.",
    "China bans crypto mining again, hash rate drops significantly.",
    "Solana network offline for 4 hours due to heavy congestion.",
    "BlackRock ETF approval brings institutional billions into crypto."
]

def json_serializer(data):
    """
    Serializes dictionary data into JSON format for Kafka.
    """
    return json.dumps(data).encode('utf-8')

def run_producer():
    """
    Main loop to simulate a real-time news feed.
    """
    producer = None
    
    # --- Retry Logic (Resilience) ---
    # Try to connect for 60 seconds (12 attempts * 5s) before failing
    for i in range(12):
        try:
            print(f"🔄 Attempting to connect to Kafka ({i+1}/12)...")
            producer = KafkaProducer(
                bootstrap_servers=[KAFKA_SERVER],
                value_serializer=json_serializer
            )
            print("✅ Successfully connected to Kafka Broker!")
            break
        except Exception as e:
            print(f"⚠️ Connection failed, retrying in 5s... Error: {e}")
            time.sleep(5)
    
    # If connection still fails after retries, exit.
    if not producer:
        print("❌ Critical Failure: Could not connect to Kafka after 60s.")
        return

    print(f"📡 Producer started. Sending news to topic '{KAFKA_TOPIC}'...")

    # --- Main Event Loop ---
    while True:
        # 1. Select a random headline
        news = random.choice(headlines)
        
        # 2. Create the payload with metadata
        payload = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'headline': news,
            'source': 'CryptoWire API'
        }
        
        # 3. Send to Kafka Topic
        producer.send(KAFKA_TOPIC, payload)
        
        # 4. Log to console
        print(f"Sent: {news[:50]}...")
        
        # 5. Wait a bit (Simulate real-time latency)
        time.sleep(random.randint(5, 10))

if __name__ == "__main__":
    run_producer()