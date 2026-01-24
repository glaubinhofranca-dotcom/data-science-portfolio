# 📈 Quantitative Portfolio Optimization Engine (Markowitz Model)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Finance](https://img.shields.io/badge/Domain-Quant%20Finance-green)
![Status](https://img.shields.io/badge/Status-Completed-success)

## 📋 Executive Summary
This project implements a **Quantitative Investment Tool** based on **Modern Portfolio Theory (Harry Markowitz)**. 

The engine uses Python to extract real-time financial data, simulate 10,000 portfolio combinations via **Monte Carlo methods**, and mathematically identify the optimal asset allocation that maximizes the **Sharpe Ratio** (Risk-Adjusted Return).

The output includes a generated **Efficient Frontier chart** and exported datasets for dashboarding in **Power BI**.

---

## 💼 Business Problem
Investors often struggle to balance **Risk vs. Return**. 
* Holding too much cash loses to inflation.
* Holding volatile stocks risks capital erosion.
* **The Challenge:** How to mathematically define the "perfect" mix of assets (Tech, Energy, Gold, Banking) to get the highest possible return for the lowest possible risk?

## 🛠️ Technical Solution & Stack
This solution moves beyond Excel limitations by using **Scientific Computing libraries** to solve non-linear optimization problems.

* **Data Ingestion:** `yfinance` (Real-time stock data from Yahoo Finance API).
* **Data Processing:** `pandas` & `numpy` (Log returns, Covariance Matrices).
* **Simulation:** **Monte Carlo Simulation** (10,000 iterations) to map the Efficient Frontier.
* **Optimization:** `scipy.optimize` (Minimize negative Sharpe Ratio).
* **Visualization:** `matplotlib` (Python Charts) & Power BI integration.

---

## 📊 Key Results (Sample Run)
The algorithm analyzed a diversified basket of assets (`AAPL`, `MSFT`, `GOOGL`, `JPM`, `XOM`, `GLD`, `TSLA`, `AMZN`) over a 2-year period.

### The Efficient Frontier
The model successfully identified the **Global Maximum Sharpe Ratio** portfolio (Red Star):

<img width="2002" height="1143" alt="Quant Finance" src="https://github.com/user-attachments/assets/27536c9a-31fb-4232-b816-804414bf429d" />


### 🏆 Optimal Allocation Strategy
Based on the specific iteration visualized in the dashboard, the algorithm suggested a heavy weight on Big Tech combined with Energy/Finance hedges:

| Asset | Ticker | Weight | Rationale (Inferred) |
| :--- | :--- | :--- | :--- |
| **Google** | `GOOGL` | **47.2%** | Primary driver of portfolio returns (High Momentum). |
| **JPMorgan** | `JPM` | **17.0%** | Financial sector exposure. |
| **Exxon Mobil** | `XOM` | **14.1%** | Inflation hedge (Energy sector). |
| **Gold** | `GLD` | **11.6%** | Defensive asset (Low correlation). |
| **Amazon** | `AMZN` | **7.5%** | Consumer cyclical play. |
| **Microsoft** | `MSFT` | **2.6%** | Stability in the Tech sector. |

**Performance Metrics:**
* **Expected Annual Return:** 32.56%
* **Annual Volatility:** 13.20%
* **Sharpe Ratio:** 2.16 (Excellent risk-adjusted performance)

---

## ⚙️ How to Run This Project

### 1. Prerequisites
Ensure you have Python installed. Install dependencies using the requirements file:

```bash
pip install yfinance pandas numpy matplotlib scipy
