# 📱 WhatsApp AI Agent (FastAPI + Twilio + LangChain)

## 📋 Project Overview
This project transforms a standard WhatsApp number into a **Context-Aware AI Assistant**. Built with **FastAPI** for high-performance webhook handling and **LangChain** for the cognitive architecture, this bot can hold real-time, memory-persistent conversations with users directly on WhatsApp.

By utilizing Twilio's Sandbox and Ngrok for secure tunneling, this Proof of Concept (PoC) demonstrates a complete end-to-end integration of Generative AI into a massive enterprise communication channel.

![alt text](chat_bot.png)

## 🏗️ Architecture & Data Flow
1. **User** sends a message on WhatsApp.
2. **Twilio** captures the message and triggers a webhook via HTTP POST.
3. **Ngrok** creates a secure tunnel forwarding the request to our local environment.
4. **FastAPI** receives the payload, extracting the `Body` (message) and `From` (phone number).
5. **LangChain (LCEL)** processes the text. The phone number acts as a unique `Session ID` to retrieve the correct **Conversation History** from memory.
6. **OpenAI (`gpt-3.5-turbo`)** generates the contextual response.
7. **FastAPI** packages the response in TwiML (XML) format and sends it back to Twilio.
8. **WhatsApp** delivers the final message to the user.

## 🛠️ Tech Stack
* **Web Framework:** FastAPI, Uvicorn
* **API Integration:** Twilio (WhatsApp Business API)
* **AI & LLM:** LangChain (Pure LCEL Pipeline), OpenAI API
* **Memory Management:** `RunnableWithMessageHistory` (Session-based memory)
* **Networking:** Ngrok (Localhost tunneling)

## 🚀 How to Run Locally

### 1. Prerequisites
* Python 3.9+
* OpenAI API Key
* A free [Twilio](https://www.twilio.com/) account
* [Ngrok](https://ngrok.com/) installed and authenticated

### 2. Environment Setup
Clone the repository and install the dependencies:
    
    git clone https://github.com/glaubinhofranca-dotcom/26_WhatsApp_AI_Bot.git

    cd 26_WhatsApp_AI_Bot
    
    pip install -r requirements.txt
    
Create a .env file in the root directory and add your OpenAI key:
    
    OPENAI_API_KEY=sk-your_actual_key_here
    
### 3. Start the Services
Run the FastAPI server:

    python bot_api.py
    
In a new terminal, start the Ngrok tunnel:

    ngrok http 8000
    

### 4. Twilio Configuration
Go to your Twilio Console -> Messaging -> Try it out -> Send a WhatsApp message.

Under the Sandbox settings tab, paste your Ngrok forwarding URL into the "WHEN A MESSAGE COMES IN" field, appending /chat at the end (e.g., https://your-ngrok-url.ngrok-free.app/chat).

Save and text the Twilio Sandbox number from your phone!

## 👤 Author
Glauber Data Science Student & Aspiring Data Engineer https://www.linkedin.com/in/glauberrocha/