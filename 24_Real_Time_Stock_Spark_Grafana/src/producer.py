import time
import json
import random
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
from datetime import datetime

# --- Configuration ---
KAFKA_BROKER = 'localhost:9092'
TOPIC_NAME = 'stock_market'
STOCKS = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']

def generate_stock_data():
    """Generates synthetic stock data."""
    symbol = random.choice(STOCKS)
    price = round(random.uniform(100.0, 1500.0), 2)
    return {
        'symbol': symbol,
        'price': price,
        'timestamp': datetime.now().isoformat(),
        'volume': random.randint(1, 100)
    }

def create_producer():
    """Tries to connect to Kafka with retries."""
    retries = 0
    while retries < 10:
        try:
            print(f"🔄 Attempting to connect to Kafka ({retries+1}/10)...")
            producer = KafkaProducer(
                bootstrap_servers=[KAFKA_BROKER],
                value_serializer=lambda x: json.dumps(x).encode('utf-8'),
                # Force protocol version to avoid negotiation errors with newer Brokers
                api_version=(0, 10, 1) 
            )
            print("✅ Connected to Kafka!")
            return producer
        except NoBrokersAvailable:
            print("⚠️ Kafka not ready yet. Retrying in 5 seconds...")
            time.sleep(5)
            retries += 1
    raise Exception("❌ Could not connect to Kafka after 10 attempts.")

def run_producer():
    producer = create_producer()

    try:
        while True:
            trade_data = generate_stock_data()
            producer.send(TOPIC_NAME, value=trade_data)
            print(f"📤 Sent: {trade_data}")
            time.sleep(0.5) # Speed of trading
            
    except KeyboardInterrupt:
        print("\n🛑 Producer stopped.")
        producer.close()

if __name__ == "__main__":
    run_producer()