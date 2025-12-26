# 🗣️ AI Agent: Text-to-SQL (Talk to Your Data)

![Python](https://img.shields.io/badge/Language-Python-blue)
![AI](https://img.shields.io/badge/AI-LangChain%20%7C%20OpenAI-green)
![DB](https://img.shields.io/badge/Database-SQLite%20%7C%20SQL-orange)

## 📋 Executive Summary
One of the biggest bottlenecks in data-driven companies is the "technical barrier": business stakeholders need answers, but data lives in SQL databases accessible only to technical staff.

This project implements a **Text-to-SQL Agent** using **LangChain** and **GPT-3.5**. It allows non-technical users to ask questions in plain English (e.g., *"Who is the employee with the highest sales?"*), which the AI automatically translates into executable SQL queries, runs against the database, and returns the simplified answer.

## 🛠️ Technical Architecture
1.  **Database:** A synthetic SQLite database (`company_data.db`) containing relational tables for Employees, Departments, and Sales.
2.  **Orchestrator:** **LangChain SQL Agent** (Zero-Shot React Description).
3.  **LLM:** **GPT-3.5 Turbo** (responsible for understanding the schema and writing the SQL syntax).
4.  **Interface:** Streamlit for real-time interaction.

## 💼 Business Value
* **Self-Service Analytics:** Empowers executives to get instant answers without waiting for data analyst tickets.
* **Productivity:** Eliminates repetitive ad-hoc SQL tasks for the data team.
* **Accessibility:** Makes data warehouses accessible to HR, Marketing, and Sales teams.

## 🚀 How to Run

### 1. Install Requirements
```bash
pip install streamlit langchain langchain-experimental langchain-openai langchain-community sqlalchemy

```

### 2. Generate the Database (Dummy Data)

Run the script to create the `company_data.db` file with realistic sample data:

```bash
python create_db.py

```

### 3. Launch the Agent

```bash
streamlit run app.py

```

---

### Author

**Glauber Rocha**
*Data Scientist & AI Engineer*