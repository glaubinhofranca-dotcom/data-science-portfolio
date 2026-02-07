import streamlit as st
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# Embeddings
from langchain_community.embeddings import HuggingFaceEmbeddings 
# LLM
from langchain_community.llms import Ollama
# Vector Store
from langchain_community.vectorstores import FAISS

# --- Page Configuration ---
st.set_page_config(page_title="FinBot: TinyLlama Edition", page_icon="🦙")

# --- Header ---
st.header("🦙 FinBot: Local AI (TinyLlama Edition)")
st.markdown("Running locally with **TinyLlama (1.1B)**. Designed for low-memory PCs.")

# --- Sidebar ---
with st.sidebar:
    st.title("Settings")
    st.info("🤖 Model: TinyLlama (1.1B)\n\n⚡ Status: Ultra-Low Memory Mode")
    uploaded_file = st.file_uploader("Upload Financial PDF", type="pdf")

# --- Main Logic ---
if uploaded_file is not None:
    pdf_reader = PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
        
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    
    st.info("🧠 Loading lightweight embeddings...")
    # Usando o mesmo embedding leve
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    if 'vector_store' not in st.session_state:
        with st.spinner("Indexing document..."):
            vector_store = FAISS.from_texts(chunks, embedding=embeddings)
            st.session_state.vector_store = vector_store
            st.success("Document Indexed!")
    
    query = st.text_input("Ask a question:")
    
    if query:
        with st.spinner("TinyLlama is thinking..."):
            docs = st.session_state.vector_store.similarity_search(query=query, k=3)
            context = "\n\n".join([doc.page_content for doc in docs])
            
            # MUDANÇA AQUI: Usando tinyllama
            llm = Ollama(model="tinyllama")
            
            prompt = f"""Use the context below to answer the question. Keep it short.
            
            Context:
            {context}
            
            Question: {query}
            
            Answer:"""
            
            response = llm.invoke(prompt)
            st.write(response)
            
            with st.expander("Context Sources"):
                st.write(context)

elif uploaded_file is None:
    st.warning("Please upload a PDF.")