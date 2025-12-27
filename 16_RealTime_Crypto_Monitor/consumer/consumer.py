import json
import psycopg2
from kafka import KafkaConsumer

# 1. Configuration
KAFKA_BROKER = 'localhost:9092'
TOPIC_NAME = 'crypto_prices'

# Database config (matches docker-compose credentials)
DB_CONFIG = {
    'dbname': 'crypto_streaming',
    'user': 'admin',
    'password': 'adminpassword',
    'host': 'localhost',
    'port': '5432'
}

def get_db_connection():
    """Establishes connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return None

def run_consumer():
    print("🚀 Starting Consumer... Listening to Kafka topic...")

    # Initialize Kafka Consumer
    consumer = KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=KAFKA_BROKER,
        auto_offset_reset='latest', # Start reading from the latest message
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    # Connect to DB
    conn = get_db_connection()
    if not conn:
        return
    
    cursor = conn.cursor()

    # Main Loop: Ingest messages
    for message in consumer:
        data = message.value
        symbol = data['symbol']
        price = data['price']
        
        # Insert into PostgreSQL
        try:
            insert_query = "INSERT INTO crypto_prices (symbol, price) VALUES (%s, %s)"
            cursor.execute(insert_query, (symbol, price))
            conn.commit() # Commit transaction
            
            print(f"💾 Saved to DB: {symbol} at ${price}")
            
        except Exception as e:
            print(f"⚠️ Error saving to DB: {e}")
            conn.rollback() # Rollback to keep connection healthy

if __name__ == '__main__':
    run_consumer()