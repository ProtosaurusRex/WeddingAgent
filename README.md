# LCA Wedding Agent

A multi-agent AI system that helps plan weddings by coordinating specialized agents for flight booking, venue selection, and playlist creation.

## Overview

The Wedding Agent is a LangChain-based application that demonstrates the power of multi-agent orchestration. It uses a hierarchical agent architecture where a main agent coordinates three specialized sub-agents:

- **Flight Agent**: Finds flight recommendations for wedding travel
- **Venue Agent**: Recommends wedding venues
- **Playlist Agent**: Suggests playlists based on preferred music genres

## Features

- **Multi-Agent Architecture**: Demonstrates how to create and orchestrate multiple AI agents working in concert
- **Web Search Integration**: Uses Tavily API for real-time web information retrieval
- **Database Queries**: Queries a playlist database for music recommendations
- **MCP Server Integration**: Integrates with Model Context Protocol (MCP) adapters
- **LangChain Framework**: Built using LangChain's agent abstractions and tools

## Project Structure

```
LCA_Wedding_Agent/
├── WeddingAgent.ipynb          # Jupyter notebook with agent definitions and execution
├── WeddingAgentPy.py           # Standalone Python script version of the wedding agent
├── requirements.txt            # Python dependencies
├── resources/
│   ├── 2.1_mcp_server.py      # Additional reference implementation
│   └── Chinook.db             # SQLite database with playlist data
└── README.md                   # This file
```

## Technical Stack

- **Framework**: [LangChain](https://python.langchain.com/)
- **Language Model**: GPT-5-nano (OpenAI)
- **Web Search**: [Tavily API](https://tavily.com/)
- **Database**: SQLite (Chinook.db for playlist data)

## Installation

### Prerequisites

- Python 3.9+
- OpenAI API key
- Tavily API key

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd LCA_Wedding_Agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
Create a `.env` file in the project root with your API keys:
```
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
```

4. Run the notebook:
Open `WeddingAgent.ipynb` in Jupyter and execute the cells sequentially.

## Usage

### Option 1: Jupyter Notebook

Open `WeddingAgent.ipynb` in Jupyter and execute the cells sequentially.

### Option 2: Standalone Python Script

Run the Python script directly:
```bash
python WeddingAgentPy.py
```

### Example Query

The main agent accepts natural language queries about wedding planning:

```python
question = "Find flight recommendations and a wedding venue for a trip from New York to London from September 1st to September 15th. The preferred genre of music for the playlist is grunge."

response = main_agent.invoke({"messages": [HumanMessage(content=question)]})
print(response['messages'][-1].content)
```

The agent will automatically:
1. Parse your request
2. Call appropriate sub-agents for flights, venues, and music
3. Aggregate and present recommendations

## Agent Architecture

### Main Agent
Coordinates all sub-agents and provides high-level wedding planning assistance.

### Sub-Agents
1. **Flight Sub-Agent** (`subagent_1`)
   - Tools: Flight agent tool, web search
   - Purpose: Find flight recommendations

2. **Venue Sub-Agent** (`subagent_2`)
   - Tools: Venue agent tool, web search
   - Purpose: Find venue recommendations

3. **Playlist Sub-Agent** (`subagent_3`)
   - Tools: Playlist agent tool, database query
   - Purpose: Find music playlist recommendations

## Key Components

### Tools Defined
- `flight_agent()`: Returns flight recommendations
- `venue_agent()`: Returns venue recommendations
- `playlist_agent()`: Returns playlist recommendations
- `web_search()`: Searches the web using Tavily API
- `query_playlist_db()`: Queries the Chinook database for playlist info
- `call_subagent_*()`: Invoke specific sub-agents from the main agent

## Learning Resources

This project was created as part of the LangChain Academy Foundation course. For more information and to learn more about LangChain, visit:

[LangChain Academy - Foundation: Introduction to LangChain (Python)](https://academy.langchain.com/courses/foundation-introduction-to-langchain-python)

## Technical Highlights

- **Tool Binding**: Demonstrates how to bind tools to agents using the `@tool` decorator
- **Sub-Agent Invocation**: Shows how to call sub-agents from within agent tools
- **LangChain Agents**: Uses `create_agent()` for agent instantiation
- **Message-Based Communication**: Leverages LangChain's message abstraction for agent communication
- **Database Integration**: Integrates SQLAlchemy-based database queries through tools

## Future Enhancements

- Add hotel booking recommendations
- Implement budget constraints and optimization
- Add guest list management
- Integrate with actual booking APIs
- Add real-time availability checking
- Implement preferences/constraints handling

## License

This project is part of the LangChain Academy curriculum.

## Support

For issues or questions, refer to:
- [LangChain Documentation](https://python.langchain.com/docs/)
- [Tavily API Documentation](https://docs.tavily.com/)

---

**Note**: This is a demonstration project showcasing multi-agent architecture patterns. In a production environment, integrate with real booking APIs and implement proper error handling, authentication, and rate limiting.
