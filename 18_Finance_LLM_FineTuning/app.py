import streamlit as st
from llama_cpp import Llama
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Financial Analyst",
    page_icon="📈",
    layout="centered"
)

# --- HEADER & SIDEBAR ---
st.title("🤖 Financial Risk AI Analyst")
st.caption("Powered by Llama-3-8B (Fine-Tuned on Credit Risk & Actuarial Data)")

with st.sidebar:
    st.header("About the Model")
    st.info(
        "This Agent utilizes a **Llama-3-8B** Large Language Model, "
        "fine-tuned specifically on financial datasets using **QLoRA**."
    )
    st.markdown("---")
    st.write("**Capabilities:**")
    st.markdown("- Basel III Regulations")
    st.markdown("- Credit Risk Assessment")
    st.markdown("- Actuarial Science Terms")

# --- MODEL LOADING (CACHED) ---
@st.cache_resource
def load_model():
    """
    Loads the quantized GGUF model efficiently.
    """
    model_name = "finance_model_llama3.gguf"
    
    if not os.path.exists(model_name):
        st.error(f"❌ Critical Error: Model file '{model_name}' not found!")
        st.warning("👉 Please download the .gguf file from your Google Drive and place it in this folder.")
        return None

    try:
        # n_ctx=2048: Context window size
        # n_gpu_layers=-1: Offload all layers to GPU (if available) for speed
        # verbose=False: Suppress low-level logs
        llm = Llama(
            model_path=model_name, 
            n_ctx=2048, 
            n_gpu_layers=-1, 
            verbose=False
        )
        return llm
    except Exception as e:
        st.error(f"❌ Error loading model: {e}")
        return None

# Load the brain
llm = load_model()

# --- CHAT LOGIC ---

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask about LGD, PD, VaR, or Insurance Policies..."):
    
    # 1. Display User Message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Generate AI Response
    if llm:
        with st.chat_message("assistant"):
            with st.spinner("Analyzing financial context..."):
                
                # Construct Prompt (Alpaca Format - Crucial for Fine-Tuned Models)
                # This matches the structure used during the training phase.
                alpaca_prompt = f"""Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
{prompt}

### Input:


### Response:
"""
                # Run Inference
                response = llm(
                    alpaca_prompt, 
                    max_tokens=512, # Allow longer technical answers
                    stop=["###", "\n\n\n"], # Stop generation at artifacts
                    temperature=0.3, # Low temperature for factual/precise answers
                    echo=False
                )
                
                bot_reply = response['choices'][0]['text']
                
                # Display and Save Assistant Message
                st.markdown(bot_reply)
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})