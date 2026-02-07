import streamlit as st
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI

# Page Config
st.set_page_config(page_title="Talk to Database", page_icon="📊")

st.title("📊 Enterprise SQL Agent")
st.markdown("Ask questions about your data in plain English. The Agent will write the SQL for you.")

# Sidebar setup
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")
    st.info("This agent uses GPT-3.5 to generate SQL queries specifically for the 'Company_Data' database.")
    
# Check for API Key
if not api_key:
    st.warning("Please enter your OpenAI API Key in the sidebar to continue.")
    st.stop()

# 1. Connect to Database
# We connect to the SQLite DB we generated
db = SQLDatabase.from_uri("sqlite:///company_data.db")

# 2. Initialize LLM (GPT-3.5 is standard for SQL)
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, api_key=api_key)

# 3. Create the SQL Agent
# "ZERO_SHOT_REACT_DESCRIPTION" allows the agent to think and query the schema
agent_executor = create_sql_agent(
    llm=llm,
    db=db,
    agent_type="openai-tools",
    verbose=True
)

# 4. Chat Interface
query = st.text_input("Ask a question (e.g., 'What is the total sales amount in the North region?')")

if query:
    with st.spinner("Analyzing database schema and generating SQL..."):
        try:
            # Run the agent
            response = agent_executor.invoke(query)
            
            # Display Answer
            st.success("Analysis Result:")
            st.write(response["output"])
            
            # Tech details (For Recruiters)
            with st.expander("🛠️ See Under the Hood (Generated SQL)"):
                st.write("The agent queried the internal SQLite database to find this answer.")
                st.info("Note: To see the exact SQL trace, look at the terminal logs (verbose=True).")
                
        except Exception as e:
            st.error(f"An error occurred: {e}")