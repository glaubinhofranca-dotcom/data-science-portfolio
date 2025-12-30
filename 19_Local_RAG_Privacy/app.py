import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import LlamaCpp
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

import streamlit as st
import tempfile
import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter 
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import LlamaCpp
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

st.title("🔐 Private Financial Analyst (Local RAG)")
st.markdown("""
**Architecture:** Llama-3 (LLM) + FAISS (Vector Store) + Sentence-Transformers (Embeddings).
**Privacy Status:** 🟢 AIR-GAPPED. No data leaves this environment.
""")

# --- Sidebar: Model & File Upload ---
with st.sidebar:
    st.header("1. Upload Document")
    uploaded_file = st.file_uploader("Upload Financial Report (PDF)", type=["pdf"])
    
    st.header("2. System Status")
    if os.path.exists("finance_model_llama3.gguf"):
        st.success("✅ Model Found (Llama-3 GGUF)")
    else:
        st.error("❌ Model NOT Found! Please move 'finance_model_llama3.gguf' to this folder.")

# --- Logic: Local RAG Pipeline ---
def process_pdf(uploaded_file):
    """
    Reads PDF, splits text into chunks, creates local embeddings, 
    and saves to a FAISS Vector Store.
    """
    # Create a temporary file to handle the upload
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file_path = tmp_file.name

    # 1. Load PDF
    loader = PyPDFLoader(tmp_file_path)
    documents = loader.load()

    # 2. Split Text (Critical for Context Window)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    text_chunks = text_splitter.split_documents(documents)

    # 3. Create Embeddings (Locally using CPU)
    # 'all-MiniLM-L6-v2' is a lightweight, high-performance local embedding model
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                       model_kwargs={'device': 'cpu'})

    # 4. Create Vector Store
    vector_store = FAISS.from_documents(text_chunks, embeddings)
    
    return vector_store

def get_llm():
    """
    Initializes the local Llama-3 model via LlamaCpp.
    """
    llm = LlamaCpp(
        model_path="finance_model_llama3.gguf",
        temperature=0.1,  # Low temperature for factual consistency
        max_tokens=512,
        n_ctx=2048,       # Context window size
        verbose=False
    )
    return llm

# --- Main Application Flow ---

if uploaded_file is not None:
    with st.spinner("Processing Document... (Creating Local Embeddings)"):
        # Build Vector Store
        vector_store = process_pdf(uploaded_file)
        st.toast("Document Vectorized Successfully!", icon="🧠")

    # Initialize the QA Chain
    llm = get_llm()
    
    # Custom Prompt for Financial Precision
    prompt_template = """Use the following pieces of context to answer the user's question.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    
    Context: {context}
    
    Question: {question}
    
    Analyst Answer:"""
    
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(search_kwargs={"k": 2}), # Retrieve top 2 chunks
        chain_type_kwargs={"prompt": PROMPT}
    )

    # Chat Interface
    st.divider()
    query = st.text_input("Ask a strategic question about the document:")

    if query:
        with st.spinner("Analyzing context..."):
            response = qa_chain.invoke(query)
            st.markdown("### 🤖 Analyst Response:")
            st.write(response['result'])
            
            with st.expander("Debugging: See Retrieved Context"):
                # Optional: Show what the model actually read from the PDF
                retrieved_docs = vector_store.search(query, search_type="similarity")
                for i, doc in enumerate(retrieved_docs):
                    st.markdown(f"**Chunk {i+1}:** {doc.page_content[:200]}...")

else:
    st.info("👈 Please upload a PDF to begin analysis.")