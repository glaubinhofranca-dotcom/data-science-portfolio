import time
import json
import random
import yfinance as yf
from kafka import KafkaProducer

# 1. Configuration
# Connecting to localhost (Hybrid Setup: Docker for Infra, Python Local)
KAFKA_BROKER = 'localhost:9092' 
TOPIC_NAME = 'crypto_prices'
SYMBOL = 'BTC-USD' # Yahoo Finance Ticker

def get_real_price():
    """
    Fetches the latest available price from Yahoo Finance API.
    """
    try:
        ticker = yf.Ticker(SYMBOL)
        # 'fast_info' provides the most recent price efficiently
        return float(ticker.fast_info['last_price'])
    except:
        return None

def run_producer():
    print(f"🚀 Starting Hybrid Producer (Real Data + Micro-Jitter) for {SYMBOL}...")
    
    # Establish connection with Kafka
    producer = None
    while producer is None:
        try:
            producer = KafkaProducer(
                bootstrap_servers=KAFKA_BROKER,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            print("✅ Connected to Kafka!")
        except Exception as e:
            print(f"⏳ Waiting for Kafka connection... Error: {e}")
            time.sleep(2)

    last_real_price = 87000.00 # Fallback initial price
    
    # Main Streaming Loop
    while True:
        # 1. Attempt to fetch real market price
        real_price = get_real_price()
        
        if real_price:
            last_real_price = real_price
        
        # 2. Add "Micro-Jitter" to simulate high-frequency volatility
        # Since Yahoo updates every ~10s, we add a random fluctuation (-$5 to +$5)
        # to keep the dashboard alive and fluid between real updates.
        jitter = random.uniform(-5.0, 5.0) 
        display_price = last_real_price + jitter

        # 3. Construct JSON Payload
        message = {
            'symbol': 'BTCUSDT',
            'price': round(display_price, 2),
            'timestamp': time.time()
        }
        
        # 4. Stream to Kafka
        try:
            producer.send(TOPIC_NAME, value=message)
            print(f"📤 Sent: ${message['price']} (Base Real Price: {last_real_price})")
        except Exception as e:
            print(f"❌ Kafka Error: {e}")
        
        # Stream every 1 second for smooth visualization
        time.sleep(1)

if __name__ == '__main__':
    run_producer()