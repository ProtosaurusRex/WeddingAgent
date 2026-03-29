import pytest
import re
from langchain.messages import HumanMessage
from WeddingAgentPy import subagent_1, subagent_2, subagent_3

def invoke_subagent(agent, prompt: str) -> str:
    result = agent.invoke({"messages": [HumanMessage(content=prompt)]})
    return result["messages"][-1].content

def count_list_items(text: str) -> int:
    """
    Count numbered list items (1. ... 2. ... 3. ...) or
    bullet points in the response text.
    """
    numbered = len(re.findall(r'^\s*\d+[.)]\s+', text, re.MULTILINE))
    bullets  = len(re.findall(r'^\s*[-•*]\s+',   text, re.MULTILINE))
    return max(numbered, bullets)

def test_flight_agent_returns_three_options():
    """Subagent 1 must return at least 3 distinct flight options."""
    response = invoke_subagent(
        subagent_1,
        "Find flights from New York to London, September 1–15."
    )
    item_count = count_list_items(response)
    assert item_count >= 3, (
        f"Expected ≥3 flight options, found {item_count}. "
        "Check the flight_agent tool docstring."
    )


def test_venue_agent_returns_three_options():
    """Subagent 2 must return at least 3 venue recommendations."""
    response = invoke_subagent(
        subagent_2,
        "Find wedding venues in London for September."
    )
    item_count = count_list_items(response)
    assert item_count >= 3, (
        f"Expected ≥3 venue options, found {item_count}. "
        "Check the venue_agent tool docstring."
    )


def test_playlist_agent_mentions_genre():
    """Subagent 3 must reference the requested genre in its response."""
    genre = "grunge"
    response = invoke_subagent(
        subagent_3,
        f"Create a wedding playlist for the genre: {genre}."
    )
    assert genre.lower() in response.lower(), (
        f"Genre '{genre}' not found in playlist response. "
        "The playlist agent may have ignored the genre constraint."
    )


def test_playlist_agent_returns_multiple_tracks():
    """Subagent 3 must suggest more than one track or artist."""
    response = invoke_subagent(
        subagent_3,
        "Create a wedding playlist for the genre: grunge."
    )
    item_count = count_list_items(response)
    assert item_count >= 2, (
        f"Expected multiple tracks/artists, found {item_count}."
    )