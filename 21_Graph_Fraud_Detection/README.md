# 🕸️ Anti-Money Laundering (AML) Graph Detector

![Status](https://img.shields.io/badge/Status-Completed-success)
![Tech](https://img.shields.io/badge/Stack-NetworkX%20%7C%20Scikit--Learn%20%7C%20PyVis-blue)
![Domain](https://img.shields.io/badge/Domain-FinTech%20%7C%20Forensics-orange)

## 📋 Executive Summary
Traditional fraud detection relies on linear rules (e.g., *"If amount > $10k, flag it"*). However, sophisticated money laundering schemes (like **Smurfing** or **Structuring**) evade these rules by breaking large sums into small, seemingly innocent transactions distributed across a network of "mules".

This project implements a **Graph Data Science** approach to detect these hidden patterns. By modeling transactions as a directed graph and applying unsupervised learning (**Isolation Forest**) on topological features (PageRank, Centrality), the system automatically flags suspicious clusters without needing labeled historical data.

## 🏗️ Technical Architecture

1.  **Graph Modeling (NetworkX):**
    * **Nodes:** Users/Accounts.
    * **Edges:** Transactions (Weighted by amount).
    * **Features:** Extracted `PageRank` (influence), `Degree Centrality` (connectivity), and `Flow Ratio` (in/out balance).

2.  **Unsupervised Anomaly Detection:**
    * **Model:** `IsolationForest` (Scikit-Learn).
    * **Logic:** Detects nodes that deviate from the "normal" topological structure of the network (e.g., hubs that route money but don't hold it).

3.  **Interactive Forensics (PyVis):**
    * Renders an interactive HTML graph where investigators can visually trace the flow of funds between suspicious entities.

## 🚀 How to Run

### 1. Generate Synthetic Data
Create a transaction log with injected fraud rings:

    python data_gen.py

### 2. Launch the Detective Dashboard

    streamlit run app.py

## 📊 Key Metrics

PageRank: Identifies "Smurfs" (intermediaries) who are structurally important in moving funds.

Flow Ratio: Detects "Pass-Through" accounts (money comes in and leaves immediately).

## 📂 Project Structure
    
    21_Graph_Fraud_Detection/
    ├── app.py                   # The Streamlit Detective App
    ├── data_gen.py              # Synthetic Data Generator (with Fraud Patterns)
    ├── transactions.csv         # Generated Data
    ├── requirements.txt         # Dependencies
    └── README.md                # Documentation

## 👨‍💻 Author
Glauber Rocha Senior Data Professional | AI Engineering