import streamlit as st
from PyPDF2 import PdfReader
# Import for text splitting
from langchain_text_splitters import RecursiveCharacterTextSplitter
# Import for FREE local embeddings (HuggingFace)
from langchain_community.embeddings import HuggingFaceEmbeddings 
# Import for FREE local LLM (Ollama)
from langchain_community.llms import Ollama
# Import for Vector Store
from langchain_community.vectorstores import FAISS

# --- Page Configuration ---
st.set_page_config(page_title="FinBot: Local AI Analyst", page_icon="💻")

# --- Header ---
st.header("💻 FinBot: Chat with 10-K (Local Phi-3)")
st.markdown("This version runs **offline** on your laptop using **Microsoft Phi-3** via Ollama.")

# --- Sidebar ---
with st.sidebar:
    st.title("Settings")
    st.info("🤖 Model: Microsoft Phi-3 (3.8B)\n\n⚡ Status: Running Locally")
    uploaded_file = st.file_uploader("Upload Financial PDF", type="pdf")
    st.divider()
    st.markdown("**Note:** First run might be slower as it loads the model into RAM.")

# --- Main Logic ---
if uploaded_file is not None:
    # 1. Read PDF
    pdf_reader = PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
        
    # 2. Split Text
    # Phi-3 handles context well, but we keep chunks moderate for speed
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    
    # 3. Create Embeddings (Free - Local CPU)
    # Using 'all-MiniLM-L6-v2' which is very fast and lightweight
    st.info("🧠 Loading embedding model to memory...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # 4. Create Vector Store (FAISS)
    if 'vector_store' not in st.session_state:
        with st.spinner("Indexing document (this runs on your CPU)..."):
            vector_store = FAISS.from_texts(chunks, embedding=embeddings)
            st.session_state.vector_store = vector_store
            st.success("Document Indexed Successfully!")
    
    # 5. Chat Interface
    query = st.text_input("Ask a question about the PDF:")
    
    if query:
        with st.spinner("Phi-3 is thinking..."):
            # Search relevant chunks
            docs = st.session_state.vector_store.similarity_search(query=query, k=3)
            context = "\n\n".join([doc.page_content for doc in docs])
            
            # Initialize Local LLM (Phi-3)
            # Make sure you ran 'ollama run phi3' in terminal before this
            llm = Ollama(model="phi3")
            
            # Prompt Construction
            prompt = f"""You are a financial analyst. Use the context below to answer the question.
            If the answer is not in the context, say you don't know.
            
            Context:
            {context}
            
            Question: {query}
            
            Answer:"""
            
            # Generate Response
            response = llm.invoke(prompt)
            st.write(response)
            
            # Show sources
            with st.expander("See source context"):
                st.write(context)

elif uploaded_file is None:
    st.warning("Please upload a PDF to start.")