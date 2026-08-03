import logging
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.services.tools import (
    search_existing_data,
    fetch_and_store_fixtures,
    fetch_and_store_team_stats,
    fetch_and_store_head_to_head,
    find_team_id,
)
from app.config import settings

logger = logging.getLogger(__name__)

llm = ChatOpenAI(
    api_key=settings.OPENAI_API_KEY,
    model="gpt-4o-mini",
    temperature=0.3
)

tools = [
    search_existing_data,
    find_team_id,
    fetch_and_store_fixtures,
    fetch_and_store_team_stats,
    fetch_and_store_head_to_head,
]

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert sports betting analyst assistant.

Your job is to answer questions about football matches, team performance,
and betting insights using real data.

Always follow this approach:
1. First, search existing data to see if relevant information is already available.
2. If you need a team's ID for any tool and are not certain of it, use find_team_id
   to look it up. Never guess a team ID.
3. If the existing data is insufficient or missing, fetch fresh data using the
   appropriate tool (fixtures, team statistics, or head-to-head).
4. After fetching new data, search existing data again to retrieve it in usable form.
5. Once you have enough context, provide a detailed, analytical answer.

Common league IDs: Premier League=39, La Liga=140, Serie A=135, Bundesliga=78.

Be transparent if you still don't have enough data after trying to fetch it.
Never make up statistics, results, or team IDs that aren't grounded in tool results."""),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

agent = create_tool_calling_agent(llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=6,
    handle_parsing_errors=True
)


def run_agent_analysis(query: str) -> str:
    try:
        logger.info(f"Running agent analysis for query: {query}")
        result = agent_executor.invoke({"input": query})
        return result["output"]
    except Exception as e:
        logger.error(f"Error during agent analysis: {e}")
        return "An error occurred during agent analysis. Please try again."