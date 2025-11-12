from agno.agent import Agent
from agno.models.groq import Groq
from agno.os import AgentOS
from agno.db.sqlite import SqliteDb
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.tavily import TavilyTools
from agno.tools.yfinance import YFinanceTools

from dotenv import load_dotenv
load_dotenv()

agent_storage: str = "tmp/agents.db"

# Web Agent - Pesquisas na internet
web_agent = Agent(
    name="Web Agent",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[TavilyTools()],
    instructions=["Always include sources", "Use Portuguese when responding"],
    # Store the agent sessions in a sqlite database
    db=SqliteDb(db_file=agent_storage),
    # Adds the current date and time to the context
    add_datetime_to_context=True,
    # Adds the history of the conversation to the messages
    add_history_to_context=True,
    # Number of history responses to add to the messages
    num_history_runs=5,
    # Adds markdown formatting to the messages
    markdown=True,
)

# Finance Agent - Análise financeira
finance_agent = Agent(
    name="Finance Agent",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[YFinanceTools()],
    instructions=["Always use tables to display data", "Use Portuguese when responding"],
    db=SqliteDb(db_file=agent_storage),
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=5,
    markdown=True,
)

# Research Agent - Pesquisas gerais com DuckDuckGo
research_agent = Agent(
    name="Research Agent",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[DuckDuckGoTools()],
    instructions=["Provide detailed research", "Always cite sources", "Use Portuguese when responding"],
    db=SqliteDb(db_file=agent_storage),
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=5,
    markdown=True,
)

# Create AgentOS with all agents
agent_os = AgentOS(agents=[web_agent, finance_agent, research_agent])
app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve("agentos:app", reload=True)

