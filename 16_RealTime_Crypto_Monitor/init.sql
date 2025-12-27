-- Create the table to store crypto prices
CREATE TABLE IF NOT EXISTS crypto_prices (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10),
    price DECIMAL(18, 8),
    event_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);