# 🤖 FinBot: Hybrid AI Financial Analyst (Cloud + Local)

![Python](https://img.shields.io/badge/Tech-OpenAI%20%7C%20Ollama-green)
![Models](https://img.shields.io/badge/LLMs-GPT3.5%20%7C%20Phi3%20%7C%20TinyLlama-blue)
![Frontend](https://img.shields.io/badge/Frontend-Streamlit-red)

## 📋 Executive Summary
Financial analysts often struggle to extract insights from dense 10-K reports.
**FinBot** is a Dual-Mode RAG Application (Retrieval-Augmented Generation) that allows users to chat with financial PDFs.

It features a **Hybrid Architecture**:
1.  **Cloud Mode (Production):** Uses OpenAI (GPT-3.5) for high-precision, client-facing answers.
2.  **Local Mode (Privacy/Dev):** Uses Ollama (TinyLlama or Phi-3) to run 100% offline and free on local hardware.

## ⚙️ Installation

1. **Install Dependencies:**
   ```bash
   pip install streamlit PyPDF2 langchain-text-splitters langchain-openai langchain-community faiss-cpu


2. **Run Cloud Mode (OpenAI):**
*Best for high accuracy. Requires an API Key.*
   ```bash
   streamlit run app.py

3. Run Local Mode - Low Memory (TinyLlama): Best for older laptops (Requires < 2GB RAM). First run: ollama run tinyllama.
   ```bash
   streamlit run app_local.py

4. Run Local Mode - Balanced (Phi-3): Best balance of speed and intelligence (Requires ~4GB RAM). First run: ollama run phi3.
   ```bash
   streamlit run app_local2.py

## 💼 Business Value

* **💰 Cost Optimization:** Use **Local mode** for development/testing and **Cloud mode** for final executive reports.
* **🔒 Data Privacy:** Local mode ensures sensitive financial data is processed entirely on-premise (offline), never leaving your secure environment.

---

### Author

**Glauber Rocha**
*Data Scientist & AI Engineer*
