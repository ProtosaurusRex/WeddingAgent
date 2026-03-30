# %%
from dotenv import load_dotenv

load_dotenv()



# %%
from langchain.tools import tool

@tool
def flight_agent(user_input: str) -> str:
    """You are a flight booking agent. Use your tool to return the top three reccomendations for flights based on user input."""
    return f"Here are flight recommendations for your input: {user_input}"

@tool
def venue_agent(user_input: str) -> str:
    """You are a venue booking agent. Use your tool to return the top three reccomendations for venues based on user input."""
    return f"Here are venue recommendations for your input: {user_input}"

@tool
def playlist_agent(user_input: str) -> str:
    """You are a playlist creating agent. Use your tool to return reccomendations for playlists based on user input."""
    return f"Here are playlist recommendations for your input: {user_input}"

# %%
from typing import Dict, Any
from tavily import TavilyClient

def get_tavily_client():
    return TavilyClient()

@tool
def web_search(query: str) -> Dict[str, Any]:

    """Search the web for information"""

    return tavily_client.search(query)


# %%
from langchain_community.utilities import SQLDatabase

db = SQLDatabase.from_uri("sqlite:///resources/Chinook.db")

@tool
def query_playlist_db(query: str) -> str:

    """Query the database for playlist information"""

    try:
        return db.run(query)
    except Exception as e:
        return f"Error querying database: {e}"

# %%
from langchain.agents import create_agent

# define llm
llm = "gpt-5-nano"

# create subagents

subagent_1 = create_agent(
    model= llm,
    tools=[flight_agent, web_search]
)

subagent_2 = create_agent(
    model = llm,
    tools = [venue_agent, web_search]
)

subagent_3 = create_agent(
    model = llm,
    tools = [playlist_agent, query_playlist_db]
)

# %%
from langchain.messages import HumanMessage

@tool
def call_subagent_1(user_input: str) -> str:
    """Call subagent 1 in order to find flight recommendations for the user input."""
    response = subagent_1.invoke({"messages": [HumanMessage(content=f"Find flight recommendations for: {user_input}")]})
    return response["messages"][-1].content

@tool
def call_subagent_2(user_input: str) -> str:
    """Call subagent 2 in order to find venue recommendations for the user input."""
    response = subagent_2.invoke({"messages": [HumanMessage(content=f"Find venue recommendations for: {user_input}")]})
    return response["messages"][-1].content

@tool
def call_subagent_3(user_input: str) -> str:
    """Call subagent 3 in order to find playlist recommendations for the user input."""
    response = subagent_3.invoke({"messages": [HumanMessage(content=f"Find playlist recommendations for: {user_input}")]})
    return response["messages"][-1].content

# %%
main_agent = create_agent(
    model='gpt-5-nano',
    tools=[call_subagent_1, call_subagent_2, call_subagent_3],
    system_prompt="You are a helpful assistant who can call subagents to help find reccomendations based on user input."
)

# %%
question = "find flight recommendations and a wedding venue for a trip from New York to London from September 1st to September 15th. The preffered genre of music for the playlist is grunge. No follow up questions. This is a hypothecitcal scenario, so you can make up the recommendations."

response = main_agent.invoke({"messages": [HumanMessage(content=question)]})

# %%
print(response['messages'][-1].content)

# %%



