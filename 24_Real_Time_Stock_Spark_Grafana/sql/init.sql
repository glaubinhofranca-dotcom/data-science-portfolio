-- Table to store aggregated stock data (Silver/Gold Layer)
CREATE TABLE IF NOT EXISTS stock_aggregates (
    window_timestamp TIMESTAMP,
    symbol VARCHAR(10),
    avg_price DOUBLE PRECISION,
    max_price DOUBLE PRECISION,
    min_price DOUBLE PRECISION,
    trade_count INT,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);