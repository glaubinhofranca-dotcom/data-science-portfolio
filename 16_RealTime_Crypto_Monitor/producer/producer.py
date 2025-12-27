import time
import json
import random
from kafka import KafkaProducer

# 1. Configuration
# Connecting to localhost because we are running outside Docker for this hybrid test
KAFKA_BROKER = 'localhost:9092' 
TOPIC_NAME = 'crypto_prices'

def generate_fake_price(last_price):
    """
    Simulates financial market using a Random Walk algorithm.
    Price fluctuates between -0.2% and +0.2% every second.
    """
    change_percent = random.uniform(-0.002, 0.002)
    return last_price * (1 + change_percent)

def run_producer():
    print("🚀 Starting Crypto Market Simulator...")
    
    # Establish connection with Kafka
    producer = None
    while producer is None:
        try:
            producer = KafkaProducer(
                bootstrap_servers=KAFKA_BROKER,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            print("✅ Connected to Kafka (Localhost)!")
        except Exception as e:
            print(f"⏳ Waiting for Kafka... Error: {e}")
            time.sleep(2)

    # Initial fictional Bitcoin price
    current_price = 95000.00 

    # Main Loop
    while True:
        # 1. Generate new price
        current_price = generate_fake_price(current_price)
        
        # 2. Create JSON payload
        message = {
            'symbol': 'BTCUSDT',
            'price': round(current_price, 2),
            'timestamp': time.time()
        }
        
        # 3. Stream to Kafka
        try:
            producer.send(TOPIC_NAME, value=message)
            print(f"📤 Sent to Kafka: {message}")
        except Exception as e:
            print(f"❌ Error sending: {e}")
        
        # Simulate real-time delay
        time.sleep(1)

if __name__ == '__main__':
    run_producer()