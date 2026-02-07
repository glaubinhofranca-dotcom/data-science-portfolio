import os
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from crewai.tools import BaseTool
from langchain_community.tools import DuckDuckGoSearchRun

# 1. Configuration
# ---------------------------------------------------------
# 🚨 SECURITY NOTE: Do NOT hardcode your API Key here if pushing to GitHub.
# Use environment variables or a placeholder string.
os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY_HERE" 

# 2. Tool Definition (Custom wrapper for compatibility)
# ---------------------------------------------------------
class SearchTool(BaseTool):
    name: str = "DuckDuckGoSearch"
    description: str = "Search the web for the latest news and information about the stock market."

    def _run(self, query: str) -> str:
        # Utilizing LangChain's tool internally
        search = DuckDuckGoSearchRun()
        return search.run(query)

# Instantiate the tool
search_tool = SearchTool()

# Initialize LLM (GPT-3.5)
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

print("🚀 Starting the Autonomous Research Team...")
ticker = "NVDA" 

# 3. Agents Definition (The Team)
# ---------------------------------------------------------

# Agent A: The Researcher
researcher = Agent(
    role='Senior Equity Researcher',
    goal=f'Uncover groundbreaking news and sentiment about {ticker}',
    backstory="""You are an expert at sniffing out the latest news in the stock market.
    You know how to distinguish real news from market noise.""",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool],
    llm=llm
)

# Agent B: The Analyst
analyst = Agent(
    role='Financial Analyst',
    goal='Analyze the news data and determine the market trend',
    backstory="""You are a seasoned Wall Street analyst. You look at data provided by the researcher
    and determine if the sentiment is Bullish (Positive) or Bearish (Negative).""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# Agent C: The Writer
writer = Agent(
    role='Financial Journalist',
    goal='Write a compelling newsletter paragraph about the findings',
    backstory="""You are a writer for Forbes or Bloomberg. You take complex financial analysis
    and turn it into an engaging story for investors.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# 4. Tasks Definition (The Workflow)
# ---------------------------------------------------------

task1 = Task(
    description=f"""Search for the latest 5 news pieces about {ticker} stock in 2024/2025.
    Focus on strategic moves, earnings, and major announcements.""",
    agent=researcher,
    expected_output="A list of key news bullet points with dates."
)

task2 = Task(
    description="""Analyze the news provided by the researcher.
    Determine the overall sentiment (Positive/Negative/Neutral) and explain why.""",
    agent=analyst,
    expected_output="A brief analysis of the market sentiment."
)

task3 = Task(
    description="""Write a short, engaging newsletter post (1 paragraph) summarizing the analysis.
    Include the ticker symbol and a 'Buy/Sell/Hold' recommendation based on the sentiment.""",
    agent=writer,
    expected_output="A polished newsletter post ready for publication."
)

# 5. Orchestration
# ---------------------------------------------------------

crew = Crew(
    agents=[researcher, analyst, writer],
    tasks=[task1, task2, task3],
    verbose=True,
    process=Process.sequential
)

# 6. Execution
# ---------------------------------------------------------
print(f"\n🤖 Assigning tasks for {ticker} analysis...\n")
result = crew.kickoff()

print("\n\n########################")
print("## FINAL REPORT ##")
print("########################\n")
print(result)