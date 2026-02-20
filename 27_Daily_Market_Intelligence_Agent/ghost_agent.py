import os
import yfinance as yf
import requests
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from twilio.rest import Client

# Load environment variables (API Keys)
load_dotenv()

# 1. Setup the Brain (LLM)
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.3)

prompt = ChatPromptTemplate.from_template("""
You are a Senior Market Intelligence Analyst.
Here is today's financial data: {finance_data}
Here are the latest geopolitical headlines: {news_data}

Write an executive "Daily Briefing" connecting the geopolitical events to potential market impacts. Be concise, professional, and structure the output with clear headings. Use WhatsApp markdown (e.g., *bold*).
""")

agent_chain = prompt | llm | StrOutputParser()

# 2. Data Collection Functions
def get_financial_data():
    print("📊 Fetching financial data...")
    tickers = ["^GSPC", "BTC-USD"] # S&P 500 and Bitcoin
    data = ""
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1d")
        if not hist.empty:
            close_price = hist['Close'].iloc[0]
            data += f"{ticker}: {close_price:.2f}\n"
    return data

def get_geopolitical_news():
    print("🌍 Fetching geopolitical news...")
    api_key = os.getenv("NEWS_API_KEY", "YOUR_NEWSAPI_KEY")
    url = f"https://newsapi.org/v2/top-headlines?category=business&language=en&apiKey={api_key}"
    
    try:
        response = requests.get(url)
        articles = response.json().get("articles", [])[:5] 
        headlines = [article["title"] for article in articles]
        return "\n".join(headlines)
    except Exception as e:
        return f"Error fetching news: {e}"

# 3. WhatsApp Delivery Function
def send_whatsapp_message(briefing_text):
    print("📲 Sending briefing to WhatsApp...")
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    from_whatsapp_number = os.getenv('TWILIO_FROM_NUMBER')
    to_whatsapp_number = os.getenv('MY_WHATSAPP_NUMBER')

    client = Client(account_sid, auth_token)

    try:
        message = client.messages.create(
            body=briefing_text,
            from_=from_whatsapp_number,
            to=to_whatsapp_number
        )
        print(f"✅ WhatsApp message delivered! Message SID: {message.sid}")
    except Exception as e:
        print(f"❌ Error sending WhatsApp message: {e}")

# 4. The Ghost's Main Routine
def daily_routine():
    print("\n" + "="*50)
    print("👻 Ghost Agent waking up! Starting data collection...")
    
    finance_data = get_financial_data()
    news_data = get_geopolitical_news()
    
    print("🧠 Processing analysis with OpenAI...")
    briefing = agent_chain.invoke({
        "finance_data": finance_data,
        "news_data": news_data
    })
    
    print("\n✅ Analysis complete! Check your terminal and your WhatsApp.\n")
    print(briefing)
    print("\n" + "="*50)
    
    # Trigger the WhatsApp delivery
    send_whatsapp_message(briefing)

# 5. Execution Block (Runs once and exits, perfect for Serverless / CRON)
if __name__ == "__main__":
    daily_routine()