import pytest


def test_langchain_imports():
    """Core LangChain symbols must resolve."""
    from langchain.tools import tool
    from langchain.agents import create_agent
    from langchain.messages import HumanMessage


def test_openai_import():
    """openai package must be installed."""
    import openai


def test_tavily_import():
    """tavily-python must be installed."""
    from tavily import TavilyClient


def test_langchain_community_import():
    """langchain-community must be installed (used for SQLDatabase)."""
    from langchain_community.utilities import SQLDatabase


def test_sqlalchemy_import():
    """SQLAlchemy must be available for SQLDatabase to work."""
    import sqlalchemy


def test_dotenv_import():
    """python-dotenv must be installed for .env loading."""
    from dotenv import load_dotenv


def test_wedding_agent_module_loads():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "WeddingAgentPy", "WeddingAgentPy.py"
    )
    assert spec is not None, "Could not locate WeddingAgentPy.py"
    assert spec.loader is not None, "Module spec has no loader"
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)