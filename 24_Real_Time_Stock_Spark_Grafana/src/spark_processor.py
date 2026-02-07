import os
import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, avg, max, min, count
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType, IntegerType

# --- PATH CONFIGURATION (ABSOLUTE) ---
# Get the absolute path of the directory where this script is located
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# Get the project root (one level up)
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
# Absolute path to the jars directory
JARS_DIR = os.path.join(PROJECT_ROOT, "jars")

# List of required JAR files
# NOTE: Commas are crucial here to prevent string merging!
REQUIRED_JARS = [
    "spark-sql-kafka-0-10_2.12-3.5.0.jar",
    "kafka-clients-3.5.1.jar",
    "postgresql-42.6.0.jar",
    "spark-token-provider-kafka-0-10_2.12-3.5.0.jar",
    "commons-pool2-2.11.1.jar"
]

# Build the full path string checking if files exist
jar_paths = []
for jar in REQUIRED_JARS:
    path = os.path.join(JARS_DIR, jar)
    if not os.path.exists(path):
        print(f"❌ CRITICAL ERROR: JAR not found: {path}")
        sys.exit(1)
    jar_paths.append(path)

# Join paths with comma (Spark format requirement)
FULL_JARS_PATH = ",".join(jar_paths)
print(f"📦 Loading Jars from: {JARS_DIR}")

# --- SPARK & DB CONFIGURATION ---
KAFKA_BROKER = "localhost:9092"
TOPIC_NAME = "stock_market"
POSTGRES_URL = "jdbc:postgresql://localhost:5436/stock_market"
POSTGRES_PROPERTIES = {
    "user": "admin",
    "password": "admin",
    "driver": "org.postgresql.Driver"
}

def write_to_postgres(df, epoch_id):
    """
    Writes the micro-batch to PostgreSQL.
    """
    print(f"💾 Writing batch {epoch_id} to Postgres...")
    try:
        df.write \
            .jdbc(url=POSTGRES_URL, table="stock_aggregates", mode="append", properties=POSTGRES_PROPERTIES)
        print("✅ Batch written successfully!")
    except Exception as e:
        print(f"❌ Error writing batch: {e}")

def run_spark_job():
    # 1. Initialize Spark Session
    # We must explicitly pass the JARs to the config
    spark = SparkSession.builder \
        .appName("StockMarketRealTimeAnalytics") \
        .config("spark.jars", FULL_JARS_PATH) \
        .config("spark.driver.extraClassPath", FULL_JARS_PATH) \
        .config("spark.sql.shuffle.partitions", "2") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")
    print("⚡ Spark Session Created Successfully!")

    # 2. Define Schema for JSON data coming from Kafka
    schema = StructType([
        StructField("symbol", StringType(), True),
        StructField("price", DoubleType(), True),
        StructField("timestamp", TimestampType(), True),
        StructField("volume", IntegerType(), True)
    ])

    # 3. Read Stream from Kafka
    print("🎧 Connecting to Kafka...")
    kafka_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BROKER) \
        .option("subscribe", TOPIC_NAME) \
        .option("startingOffsets", "latest") \
        .load()

    # 4. Parse JSON and Apply Transformations
    parsed_df = kafka_df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")

    # 5. Aggregate Data (Gold Layer Logic)
    # Group by 1-minute window and symbol
    aggregated_df = parsed_df \
        .withWatermark("timestamp", "1 minute") \
        .groupBy(
            window(col("timestamp"), "1 minute"),
            col("symbol")
        ) \
        .agg(
            avg("price").alias("avg_price"),
            max("price").alias("max_price"),
            min("price").alias("min_price"),
            count("price").alias("trade_count")
        ) \
        .select(
            col("window.start").alias("window_timestamp"),
            col("symbol"),
            col("avg_price"),
            col("max_price"),
            col("min_price"),
            col("trade_count")
        )

    # 6. Write Stream to Postgres
    # Using 'update' mode to emit results as soon as the window updates
    query = aggregated_df.writeStream \
        .outputMode("update") \
        .foreachBatch(write_to_postgres) \
        .start()

    print("🌊 Streaming started... Waiting for data...")
    query.awaitTermination()

if __name__ == "__main__":
    run_spark_job()