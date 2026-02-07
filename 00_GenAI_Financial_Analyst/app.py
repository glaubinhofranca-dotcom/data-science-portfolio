import streamlit as st
from PyPDF2 import PdfReader
# Updated import for text splitting
from langchain_text_splitters import RecursiveCharacterTextSplitter
# Updated imports for OpenAI models and embeddings
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
# Updated import for Vector Store (FAISS)
from langchain_community.vectorstores import FAISS

# --- Page Configuration ---
st.set_page_config(page_title="FinBot: AI Financial Analyst", page_icon="🤖")

# --- Header ---
st.header("🤖 FinBot: Chat with Financial Reports (10-K)")
st.markdown("Upload a PDF (e.g., Tesla 10-K) and ask questions like *'What are the main risk factors?'*")

# --- Sidebar ---
with st.sidebar:
    st.title("Settings")
    api_key = st.text_input("Enter OpenAI API Key:", type="password")
    st.markdown("[Get an OpenAI API Key](https://platform.openai.com/account/api-keys)")
    uploaded_file = st.file_uploader("Upload Financial PDF", type="pdf")
    
    st.divider()
    st.markdown("**Status:** using OpenAI GPT-3.5-Turbo")

# --- Main Logic ---
if uploaded_file is not None and api_key:
    # 1. Read PDF
    pdf_reader = PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
        
    # 2. Split Text (Chunks)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    
    # 3. Create Embeddings (Uses a small amount of OpenAI credits)
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    
    # 4. Create Vector Store (FAISS)
    if 'vector_store' not in st.session_state:
        with st.spinner("Indexing document..."):
            vector_store = FAISS.from_texts(chunks, embedding=embeddings)
            st.session_state.vector_store = vector_store
            st.success("Document Analyzed!")
    
    # 5. Chat Interface
    query = st.text_input("Ask a question:")
    
    if query:
        with st.spinner("Analyzing..."):
            # Search for relevant chunks
            docs = st.session_state.vector_store.similarity_search(query=query, k=3)
            
            # Initialize LLM
            llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=api_key, temperature=0)
            
            # Manually Construct Prompt (More robust than old Chains)
            context_text = "\n\n".join([doc.page_content for doc in docs])
            
            prompt = f"""You are a senior financial analyst. Answer the question based ONLY on the context below.
            
            Context:
            {context_text}
            
            Question: {query}
            
            Answer:"""
            
            # FIX: Using invoke() instead of predict() for newer LangChain versions
            response_message = llm.invoke(prompt)
            st.write(response_message.content)
            
            # Show sources for transparency
            with st.expander("See source context"):
                st.write(context_text)

elif uploaded_file is not None and not api_key:
    st.warning("Please enter your OpenAI API Key in the sidebar.")