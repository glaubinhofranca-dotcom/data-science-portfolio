## 📉 Real-Time Crypto Trade Monitor (Streaming Architecture)

![Architecture](https://img.shields.io/badge/Architecture-Event%20Driven-blue)
![Stack](https://img.shields.io/badge/Tech-Kafka%20%7C%20Docker%20%7C%20PowerBI-orange)
![Data](https://img.shields.io/badge/Source-Yahoo%20Finance%20API-green)

## 📋 Executive Summary
This project demonstrates a robust **Real-Time Data Engineering Pipeline** designed to ingest, process, and visualize cryptocurrency market data.

Unlike simple static dashboards, this architecture utilizes **Apache Kafka** for event streaming and connects to **Financial APIs (Yahoo Finance)** to fetch real-world data. It implements an **SQL Aggregation Layer** to transform raw ticks into professional **OHLC Candlestick Charts** instantly.

---

## 🏗️ Technical Architecture

The pipeline consists of 5 main components orchestrated via **Docker**:

1.  **Source (Hybrid Producer):** A Python microservice that fetches **Real-Time Data** from Yahoo Finance API. It applies a *Micro-Jitter* algorithm to simulate high-frequency trading volatility between API updates.
2.  **Message Broker:** **Apache Kafka** (running on Docker) acts as the central nervous system, buffering and distributing messages.
3.  **Ingestion (Consumer):** A dedicated Python worker that subscribes to the Kafka topic and persists data to storage.
4.  **Storage & Transformation:** **PostgreSQL** database running in a container. It includes an **Automated SQL View** that aggregates raw data into 1-minute OHLC (Open, High, Low, Close) candles.
5.  **Visualization:** **Power BI** connected via **DirectQuery**, rendering professional Candlestick charts that update live.

---

## 🚀 How to Run

### 1. Infrastructure Setup (Docker)
Ensure Docker Desktop is running, then spin up the environment (Kafka, Zookeeper, Postgres):

    docker-compose up -d

### 2. Environment Configuration
Create a virtual environment and install the required Python drivers (including yfinance):

    pip install kafka-python psycopg2-binary requests yfinance

### 3. Execution Pipeline
Step A: Start the Producer Open a terminal to start streaming real market data:

    python producer/producer.py

Step B: Start the Consumer Open a second terminal to start persisting data to SQL:
    
    python consumer/consumer.py

### 4. Visualization (Power BI)

1. Open Power BI Desktop.

2. Get Data -> PostgreSQL Database.

3. Server: localhost | Database: crypto_streaming.

4. Important: Select DirectQuery mode.

5. Connect to the view_crypto_candles view for the Candlestick chart (or crypto_prices for raw ticks).

## 📂 Project Structure

    16_RealTime_Crypto_Monitor/
    ├── consumer/
    │   └── consumer.py       # Ingests data from Kafka -> PostgreSQL
    ├── producer/
    │   └── producer.py       # Fetches Yahoo Finance Data -> Sends to Kafka
    ├── docker-compose.yml    # Infrastructure Orchestration (Kafka, ZK, DB)
    ├── init.sql              # Database Schema & Candlestick View definition
    └── README.md             # Documentation

## 👨‍💻 Author
Glauber Rocha Senior Data Professional | AI & Engineering
