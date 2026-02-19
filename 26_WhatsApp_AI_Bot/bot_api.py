import os
from fastapi import FastAPI, Form
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse

# LangChain Imports
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# 1. Initialize FastAPI App
app = FastAPI(title="WhatsApp AI Agent API with Memory")

# 2. Setup the LLM
from dotenv import load_dotenv
load_dotenv() # This loads the API key from the .env file automatically

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.5)

# 3. Setup Prompt with Memory Placeholder
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful, smart, and concise AI assistant communicating via WhatsApp. Keep your answers short and format them using WhatsApp markdown (e.g., *bold*, _italics_)."),
    MessagesPlaceholder(variable_name="history"), # <-- Conversation history goes here!
    ("human", "{message}")
])

agent_chain = prompt | llm | StrOutputParser()

# 4. --- MEMORY SETUP ---
# In-memory dictionary to store the conversation history for each phone number
store = {}

def get_session_history(session_id: str) -> ChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory() # Creates a new memory state if the phone number is new
    return store[session_id]

# Wraps our Agent with the ability to read and write to memory
agent_with_memory = RunnableWithMessageHistory(
    agent_chain,
    get_session_history,
    input_messages_key="message",
    history_messages_key="history",
)

# 5. Create the Webhook Endpoint
@app.post("/chat")
async def whatsapp_webhook(Body: str = Form(...), From: str = Form(...)):
    """
    Body = The text of the user's message
    From = The user's phone number (used as the Session ID)
    """
    print(f"📥 Received from {From}: {Body}")
    
    try:
        # Calls the AI passing the phone number as 'session_id'
        ai_response = agent_with_memory.invoke(
            {"message": Body},
            config={"configurable": {"session_id": From}}
        )
        print(f"🤖 AI Response: {ai_response}")
        
    except Exception as e:
        ai_response = f"❌ Sorry, my AI brain encountered an error: {str(e)}"
        print(ai_response)

    # Format the response for Twilio (TwiML)
    twilio_response = MessagingResponse()
    twilio_response.message(ai_response)
    
    return Response(content=str(twilio_response), media_type="application/xml")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)