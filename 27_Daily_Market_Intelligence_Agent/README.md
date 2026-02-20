# 👻 Ghost AI: Daily Market Intelligence Agent

## 📋 Project Overview
An event-driven, autonomous AI agent that runs silently in the background to provide daily executive market briefings. This "Ghost Agent" automatically fetches real-time financial market data and top geopolitical news, processes the information through a Large Language Model (LLM) to analyze potential market impacts, and delivers the final briefing directly to the user's phone via WhatsApp.

This project demonstrates skills in **Background Task Scheduling**, **Data Ingestion (APIs)**, **GenAI Analysis**, and **Automated Alerting Systems**.

## 🏗️ Architecture & Data Flow
1. **The Scheduler:** Python's `schedule` library acts as a CRON job, waking the agent up at a specific time every day.
2. **Data Ingestion:**
   * **Finance:** `yfinance` fetches the latest closing prices for key indicators (e.g., S&P 500, Bitcoin).
   * **Geopolitics:** `NewsAPI` retrieves the top 5 global business/geopolitical headlines.
3. **Cognitive Engine (LangChain + OpenAI):** The raw data is fed into `gpt-3.5-turbo` with a custom prompt instructing it to act as a Senior Market Analyst and correlate the news with market trends.
4. **Delivery (Twilio):** The finalized executive briefing is sent out programmatically to the user's WhatsApp via the Twilio REST API.

## 🛠️ Tech Stack
* **Language:** Python
* **AI & LLM:** LangChain, OpenAI API
* **Financial Data:** `yfinance`
* **News Data:** `requests` (NewsAPI)
* **Messaging/Alerts:** Twilio API (WhatsApp)
* **Automation:** `schedule`

## 🚀 How to Run Locally

### 1. Prerequisites
* Python 3.9+
* API Keys for OpenAI, NewsAPI, and Twilio

### 2. Environment Setup
Clone the repository and install the dependencies:

    git clone https://github.com/glaubinhofranca-dotcom/27_Daily_Market_Intelligence_Agent.git
    cd 27_Daily_Market_Intelligence_Agent
    pip install -r requirements.txt

Create a .env file in the root directory:

    OPENAI_API_KEY=sk-your_openai_key
    NEWS_API_KEY=your_newsapi_key
    TWILIO_ACCOUNT_SID=your_twilio_sid
    TWILIO_AUTH_TOKEN=your_twilio_token
    TWILIO_FROM_NUMBER=whatsapp:+14155238886
    MY_WHATSAPP_NUMBER=whatsapp:+1YOURNUMBER

### 3. Start the Ghost Agent
Run the script. It will remain active in your terminal/background and execute the routine at the scheduled time.

    python ghost_agent.py

## 👤 Author
Glauber Data Science Student & Aspiring Data Engineer https://www.linkedin.com/in/glauberrocha/