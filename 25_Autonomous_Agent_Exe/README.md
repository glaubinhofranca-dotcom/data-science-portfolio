# 🤖 Autonomous RAG Agent (Desktop Executable)

## 📋 Project Overview
This project is a standalone desktop application that acts as a local **Retrieval-Augmented Generation (RAG) AI Agent**. Built with the modern **LangChain Expression Language (LCEL)** architecture, it allows users to load their own documents (PDF, DOCX, XLSX) and ask questions about the content without needing to open a terminal or install Python.

The application is packaged into a standalone `.exe` using PyInstaller, making it easily distributable for business and enterprise environments.

## 🛠️ Tech Stack
* **UI/UX:** CustomTkinter (Modern Native Windows Interface)
* **AI & LLM:** LangChain (Pure LCEL Pipeline), OpenAI API (`gpt-3.5-turbo`)
* **Vector Database:** FAISS (In-memory retrieval)
* **Document Parsing:** PyPDF2, python-docx, Pandas
* **Deployment:** PyInstaller (Standalone Executable Packaging)

## 🏗️ Architecture (LCEL Pipeline)
The agent utilizes a state-of-the-art data flow:
`Document Loaders -> RecursiveCharacterTextSplitter -> FAISS Embeddings -> Retriever -> Prompt Template -> ChatOpenAI -> StrOutputParser`

## 🚀 How to Run from Source

### Prerequisites
* Python 3.9+
* OpenAI API Key

### Steps
1. Clone the repository:
   ```bash
   git clone [https://github.com/glaubinhofranca-dotcom/25_Autonomous_Agent_Exe.git](https://github.com/glaubinhofranca-dotcom/25_Autonomous_Agent_Exe.git)
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python document_agent.py
   ```
### (Note: To compile the standalone executable, run the PyInstaller command with the appropriate hidden imports for LangChain and CustomTkinter).

## 👤 Author
Glauber Data Science Student & Aspiring Data Engineer https://www.linkedin.com/in/glauberrocha/