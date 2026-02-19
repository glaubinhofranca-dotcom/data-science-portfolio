import os
import pandas as pd
import docx
from PyPDF2 import PdfReader

import customtkinter as ctk
from tkinter import filedialog, messagebox

# --- Pure LCEL LangChain Imports (No 'chains' module needed) ---
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# --- UI Configuration (Dark Mode) ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class DocumentReaderAgentApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AI Agent - Document Reader")
        self.geometry("850x650")
        self.vector_store = None

        # --- LAYOUT: SIDEBAR (Settings & Files) ---
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        self.lbl_api = ctk.CTkLabel(self.sidebar, text="OpenAI API Key:", font=("Arial", 14, "bold"))
        self.lbl_api.pack(pady=(20, 5), padx=10)

        self.api_entry = ctk.CTkEntry(self.sidebar, placeholder_text="sk-...", show="*")
        self.api_entry.pack(pady=5, padx=10, fill="x")

        self.btn_load = ctk.CTkButton(self.sidebar, text="📁 Load Files", command=self.load_files)
        self.btn_load.pack(pady=20, padx=10, fill="x")

        self.lbl_status = ctk.CTkLabel(self.sidebar, text="No files loaded.", text_color="gray")
        self.lbl_status.pack(pady=5, padx=10)

        # --- LAYOUT: MAIN AREA (Chat Interface) ---
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.chat_history = ctk.CTkTextbox(self.main_frame, state="disabled", wrap="word", font=("Arial", 14))
        self.chat_history.pack(fill="both", expand=True, pady=(0, 10))

        self.input_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.input_frame.pack(fill="x")

        self.txt_question = ctk.CTkEntry(self.input_frame, placeholder_text="Ask something about the documents...", height=40)
        self.txt_question.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.txt_question.bind("<Return>", lambda event: self.ask_question())

        self.btn_send = ctk.CTkButton(self.input_frame, text="Send", width=80, height=40, command=self.ask_question)
        self.btn_send.pack(side="right")

        self.write_chat("🤖 Agent: Hello! Please insert your OpenAI API Key, load your documents, and ask me anything.")

    def write_chat(self, text):
        """Helper function to append text to the chat window."""
        self.chat_history.configure(state="normal")
        self.chat_history.insert("end", text + "\n\n")
        self.chat_history.configure(state="disabled")
        self.chat_history.yview("end") 

    def extract_text(self, file_paths):
        """Reads PDF, DOCX, and XLSX files and concatenates their content."""
        full_text = ""
        for path in file_paths:
            ext = os.path.splitext(path)[1].lower()
            try:
                if ext == ".pdf":
                    pdf = PdfReader(path)
                    for page in pdf.pages:
                        extracted = page.extract_text()
                        if extracted:
                            full_text += extracted + "\n"
                elif ext == ".docx":
                    doc = docx.Document(path)
                    for para in doc.paragraphs:
                        full_text += para.text + "\n"
                elif ext == ".xlsx":
                    df = pd.read_excel(path)
                    full_text += df.to_string() + "\n"
            except Exception as e:
                messagebox.showerror("Read Error", f"Error reading {os.path.basename(path)}: {str(e)}")
        return full_text

    def load_files(self):
        """Extracts text and builds the FAISS Vector Database."""
        api_key = self.api_entry.get().strip()
        if not api_key:
            messagebox.showwarning("Warning", "Please insert your OpenAI API Key first.")
            return

        file_paths = filedialog.askopenfilenames(
            title="Select Documents",
            filetypes=[("Documents", "*.pdf *.docx *.xlsx")]
        )
        
        if not file_paths: 
            return

        self.lbl_status.configure(text="Processing...", text_color="orange")
        self.update() 

        # 1. Extract Raw Text
        raw_text = self.extract_text(file_paths)
        if not raw_text.strip():
            self.lbl_status.configure(text="Files are empty.", text_color="red")
            return

        # 2. Split into Chunks
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_text(raw_text)

        # 3. Create FAISS Vector Store
        try:
            os.environ["OPENAI_API_KEY"] = api_key
            embeddings = OpenAIEmbeddings()
            self.vector_store = FAISS.from_texts(chunks, embeddings)
            
            file_names = [os.path.basename(p) for p in file_paths]
            self.lbl_status.configure(text=f"{len(file_paths)} file(s) ready!", text_color="green")
            self.write_chat(f"📂 Files loaded successfully: {', '.join(file_names)}")
        
        except Exception as e:
            messagebox.showerror("OpenAI Error", f"Failed to generate embeddings.\n{str(e)}")
            self.lbl_status.configure(text="API Error.", text_color="red")

    def format_docs(self, docs):
        """Helper to format retrieved documents into a single string."""
        return "\n\n".join(doc.page_content for doc in docs)

    def ask_question(self):
        """Retrieves context and generates an answer using Pure LCEL architecture."""
        question = self.txt_question.get().strip()
        if not question: 
            return
        
        if not self.vector_store:
            messagebox.showwarning("Warning", "Please load documents before asking questions!")
            return

        self.txt_question.delete(0, "end")
        self.write_chat(f"👤 You: {question}")
        self.update()

        try:
            # 1. Setup the LLM
            llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
            
            # 2. Setup the Prompt Template
            template = """
            Answer the following question based ONLY on the provided context.
            If the answer is not in the context, say that you don't know.

            Context:
            {context}

            Question: {question}
            """
            prompt = ChatPromptTemplate.from_template(template)
            
            # 3. Setup Retriever
            retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})
            
            # 4. Build the Pure LCEL Pipeline (Data Flow: Retriever -> Prompt -> LLM -> String)
            rag_chain = (
                {"context": retriever | self.format_docs, "question": RunnablePassthrough()}
                | prompt
                | llm
                | StrOutputParser()
            )
            
            # 5. Invoke the pipeline
            answer = rag_chain.invoke(question)
            
            self.write_chat(f"🤖 Agent: {answer}")
        
        except Exception as e:
            self.write_chat(f"❌ Error generating response: {str(e)}")

if __name__ == "__main__":
    app = DocumentReaderAgentApp()
    app.mainloop()