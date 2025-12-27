# 🕵️‍♂️ Multi-Agent System: Autonomous Equity Research

![Python](https://img.shields.io/badge/Language-Python-blue)
![AI](https://img.shields.io/badge/Framework-CrewAI%20%7C%20LangChain-green)
![Agents](https://img.shields.io/badge/Agents-Autonomous-orange)

## 📋 Executive Summary
Standard AI Chatbots are "passive"—they wait for input. **Autonomous Agents** are "active"—they utilize tools and collaborate to achieve a complex goal.

This project utilizes **CrewAI** to orchestrate a team of 3 specialized AI Agents that act as an **Automated Investment Committee**:
1.  **The Researcher:** Scrapes the web for real-time news (using DuckDuckGo) to find strategic moves and earnings reports.
2.  **The Analyst:** Interprets market sentiment (Bullish/Bearish) and identifies risks.
3.  **The Journalist:** Synthesizes the technical analysis into a compelling newsletter format.

## 🛠️ Technical Architecture
* **Orchestration Framework:** CrewAI (Agentic Workflow).
* **LLM:** OpenAI GPT-3.5 Turbo.
* **Tools:** Custom implementation of DuckDuckGo Search (wrapped for CrewAI compatibility).
* **Process:** Sequential Logic (Research -> Analysis -> Drafting).

## 🚀 How to Run

### 1. Environment Setup
It is recommended to use **Python 3.11** to ensure compatibility with CrewAI dependencies.
    ```bash
    conda create -n portfolio_ai python=3.11
    conda activate portfolio_ai

### 2. Install Dependencies
    ```Bash
    pip install crewai langchain-openai langchain-community duckduckgo-search

### 3. Configuration
    Open main.py and set your OpenAI API Key:
    Python
    os.environ["OPENAI_API_KEY"] = "YOUR_KEY_HERE"

### 4. Execution
    Run the orchestration script:
    ```Bash
    python main.py
    The agents will automatically start the research process for the defined ticker (default: NVDA).

📂 Project Structure
main.py: Contains the Agents, Tasks, and Custom Tool definitions.
README.md: Documentation.

Author
Glauber Rocha Senior Data Professional | AI Engineer
