# ⚡ Real-Time AI Sentiment Trader (Kafka + Llama-3)

![Status](https://img.shields.io/badge/Status-Live-green)
![Tech](https://img.shields.io/badge/Stack-Kafka%20%7C%20Llama3%20%7C%20Docker-blue)
![Architecture](https://img.shields.io/badge/Arch-Event--Driven-orange)

## 📋 Executive Summary
This project bridges the gap between **Big Data Engineering** and **Generative AI**.
It implements a real-time streaming pipeline that ingests financial news, processes it instantly using a local LLM (Llama-3), and visualizes the market sentiment (Bullish/Bearish) on a live dashboard.

Unlike static analysis, this system is designed for **High-Frequency Decision Making**, demonstrating how to integrate Large Language Models into low-latency event loops using **Apache Kafka**.

## 🏗️ Technical Architecture

1.  **Event Backbone (Apache Kafka):**
    * Runs on **Docker** containers (Zookeeper + Broker).
    * Handles high-throughput ingestion of news data via the `crypto_news` topic.

2.  **AI Inference Engine (Llama-3):**
    * **Model:** Llama-3-8B (Quantized GGUF).
    * **Optimization:** Runs locally via `llama.cpp` using CPU threading for sub-second inference.
    * **Task:** Zero-Shot Sentiment Classification (Bullish/Bearish/Neutral).

3.  **Real-Time Dashboard (Streamlit):**
    * Acts as a **Kafka Consumer**.
    * Auto-updates the UI as soon as new messages arrive in the topic.

## 🚀 How to Run

### 1. Infrastructure (Docker)
Start the Kafka message broker:
    
    docker-compose up -d

### 2. The Brain (Consumer)
Launch the Dashboard that hosts the AI model:

    streamlit run app.py

### 3. The Feed (Producer)
In a separate terminal, start generating live news:

    python producer.py

## 🧠 Example Output
News: "SEC announces strict regulations on DeFi protocols"

AI Verdict: 🔴 BEARISH (Detected instantaneously)

## 📂 Project Structure

    20_RealTime_Llama_Kafka/
    ├── app.py                   # Streamlit Consumer + Llama-3
    ├── producer.py              # News Generator (Kafka Producer)
    ├── docker-compose.yml       # Kafka Infrastructure
    ├── finance_model_llama3.gguf # The AI Model (GitIgnored)
    └── README.md                # Documentation

## 👨‍💻 Author
Glauber Rocha Senior Data Professional | AI Engineering