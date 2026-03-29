import pytest
from langchain.messages import HumanMessage
from WeddingAgentPy import main_agent

# Fixed canonical question — never change this in CI
CANONICAL_QUESTION = (
    "Find flight recommendations and a wedding venue for a trip "
    "from New York to London from September 1st to September 15th. "
    "The preferred genre of music for the playlist is grunge. "
    "No follow up questions. This is a hypothetical scenario, "
    "so you can make up the recommendations."
)

# Sub-agent tool names to look for in the message trace
REQUIRED_TOOLS = {
    "call_subagent_1",  # Flight agent
    "call_subagent_2",  # Venue agent
    "call_subagent_3",  # Playlist agent
}

# Keywords that must appear in the final response
REQUIRED_KEYWORDS = ["flight", "venue", "playlist"]

@pytest.fixture(scope="session")
def agent_response():
    """Run the agent once and share the result across all tests."""
    return main_agent.invoke({
        "messages": [HumanMessage(content=CANONICAL_QUESTION)]
    })

def test_all_subagents_called(agent_response):
    """Use Case 3: Verify tool coverage — all sub-agents must be invoked."""
    messages = agent_response["messages"]

    # Collect tool names from ToolMessage or AIMessage tool_calls
    called_tools = set()
    for msg in messages:
        if hasattr(msg, "tool_calls"):
            for tc in msg.tool_calls:
                called_tools.add(tc["name"])
        if hasattr(msg, "name") and msg.name:
            called_tools.add(msg.name)

    missing = REQUIRED_TOOLS - called_tools
    assert not missing, (
        f"Missing tool calls: {missing}. "
        "A prompt change may have broken agent routing."
    )

def test_response_contains_all_domains(agent_response):
    """Use Case 1: Verify prompt regression — final response covers all domains."""
    final_text = agent_response["messages"][-1].content.lower()

    for keyword in REQUIRED_KEYWORDS:
        assert keyword in final_text, (
            f"Keyword '{keyword}' not found in response. "
            "A prompt change may have caused the agent to drop a domain."
        )