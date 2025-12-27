# 📉 Real-Time Crypto Trade Monitor (Streaming Architecture)

![Architecture](https://img.shields.io/badge/Architecture-Event%20Driven-blue)
![Stack](https://img.shields.io/badge/Tech-Kafka%20%7C%20Docker%20%7C%20PowerBI-orange)
![Status](https://img.shields.io/badge/Status-Active-success)

## 📋 Executive Summary
This project demonstrates a robust **Real-Time Data Engineering Pipeline** designed to ingest, process, and visualize cryptocurrency market data with sub-second latency.

Moving away from traditional Batch Processing (ETL), this architecture utilizes **Apache Kafka** for high-throughput event streaming, proving the capability to handle modern "Big Data" velocity requirements. The data is persisted in a relational database and visualized via a **DirectQuery** dashboard.

---

## 🏗️ Technical Architecture

The pipeline consists of 5 main components orchestrated via **Docker**:

1.  **Source (Producer):** A Python microservice that generates/simulates high-frequency market trades (Random Walk algorithm).
2.  **Message Broker:** **Apache Kafka** (running on Docker) acts as the central nervous system, buffering and distributing messages.
3.  **Ingestion (Consumer):** A dedicated Python worker that subscribes to the Kafka topic and writes data to storage.
4.  **Storage:** **PostgreSQL** database (simulating AWS RDS) running in a container.
5.  **Visualization:** **Power BI** connected via **DirectQuery** to reflect database changes instantly without manual refresh.

---

## 🚀 How to Run

### 1. Infrastructure Setup (Docker)
Ensure Docker Desktop is running, then spin up the environment (Kafka, Zookeeper, Postgres):
```bash
docker-compose up -d

---

### 2. Environment Configuration
Create a virtual environment and install the required Python drivers:
```Bash
pip install kafka-python psycopg2-binary requests

---

### 3. Execution Pipeline
Step A: Start the Producer Open a terminal to start generating market data:
```Bash
python producer/producer.py

Step B: Start the Consumer Open a second terminal to start persisting data to SQL:
```Bash
python consumer/consumer.py

---

### 4. Visualization (Power BI)
Open Power BI Desktop.

Get Data -> PostgreSQL Database.

Server: localhost | Database: crypto_streaming.

Important: Select DirectQuery mode.

Build your dashboard using the crypto_prices table.

---

## 📂 Project Structure
Plaintext

16_RealTime_Crypto_Monitor/
├── consumer/
│   └── consumer.py       # Ingests data from Kafka -> PostgreSQL
├── producer/
│   └── producer.py       # Generates data -> Sends to Kafka
├── docker-compose.yml    # Infrastructure Orchestration (Kafka, ZK, DB)
├── init.sql              # Database Schema definition
└── README.md             # Documentation

---

## 👨‍💻 Author
Glauber Rocha Senior Data Professional | AI & Engineering