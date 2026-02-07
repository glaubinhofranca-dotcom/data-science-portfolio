# 🔒 Private Financial Analyst (Local RAG)

![Status](https://img.shields.io/badge/Status-Completed-success)
![Privacy](https://img.shields.io/badge/Privacy-Air--Gapped%20%7C%20Offline-green)
![Tech](https://img.shields.io/badge/AI-Llama3%20%7C%20LangChain%20%7C%20FAISS-blue)

## 📋 Executive Summary
This project implements a **100% Private & Offline** Retrieval-Augmented Generation (RAG) system tailored for sensitive financial documents.

Unlike standard RAG solutions that rely on external APIs (OpenAI/Anthropic), this architecture runs entirely on local infrastructure. It uses **Llama-3 (Quantized)** for reasoning and **Sentence-Transformers** for local embedding generation, ensuring that **no proprietary data ever leaves the secure environment**.

## 🏗️ Technical Architecture

1.  **Ingestion Engine:**
    * **Loader:** `PyPDFLoader` to parse complex financial reports (10-Ks, Balance Sheets).
    * **Chunking:** `RecursiveCharacterTextSplitter` to optimize context windows.

2.  **Local Vector Store (The "Vault"):**
    * **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2` (Runs locally on CPU).
    * **Database:** **FAISS** (Facebook AI Similarity Search) for high-speed local vector retrieval.

3.  **Inference Core:**
    * **Model:** Llama-3-8B (GGUF Quantized via `llama.cpp`).
    * **Orchestrator:** LangChain `RetrievalQA` chain.

## 🛡️ Privacy & Security Features
| Feature | Standard Cloud RAG | This Local RAG |
| :--- | :--- | :--- |
| **Data Transmission** | Sends PDFs to API Endpoints | **Zero Transmission (Air-Gapped)** |
| **Embeddings** | Generated on Cloud (OpenAI) | **Generated Locally (CPU)** |
| **Model Weight** | Proprietary / Black Box | **Open Weights (Llama-3)** |

## 🚀 How to Run

### 1. Prerequisites
* Python 3.11+
* **Model:** Place `finance_model_llama3.gguf` in the root directory.

### 2. Installation

    pip install -r requirements.txt

### 3. Launch the Secure Terminal

    streamlit run app.py

### 4. Usage

Upload any PDF (e.g., Tesla Q3 Report).

Watch the system create a local vector index (Status: "Vectorized Successfully").

Ask strategic questions: "What are the key risks mentioned on page 4?"

## 📂 Project Structure

    19_Local_RAG_Privacy/
    ├── app.py                   # Secure Streamlit Interface
    ├── finance_model_llama3.gguf # The "Brain" (GitIgnored)
    ├── requirements.txt         # Dependencies (LangChain, FAISS)
    └── README.md                # Documentation

## 👨‍💻 Author
Glauber Rocha Senior Data Professional | AI Engineering