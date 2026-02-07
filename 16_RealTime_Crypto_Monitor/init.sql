-- 1. Create the raw transactions table
CREATE TABLE IF NOT EXISTS crypto_prices (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10),
    price DECIMAL(18, 8),
    event_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Create the Candlestick View (OHLC - Open, High, Low, Close)
-- This aggregates raw tick data into 1-minute intervals for Power BI
CREATE OR REPLACE VIEW view_crypto_candles AS
SELECT
    date_trunc('minute', event_time) as candle_time,
    MAX(price) as high_price,
    MIN(price) as low_price,
    (ARRAY_AGG(price ORDER BY event_time ASC))[1] as open_price,
    (ARRAY_AGG(price ORDER BY event_time DESC))[1] as close_price
FROM crypto_prices
GROUP BY 1
ORDER BY 1 DESC;