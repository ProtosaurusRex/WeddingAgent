import json, pytest
from pathlib import Path
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from WeddingAgentPy import call_subagent_1, call_subagent_2, call_subagent_3

QUESTION = (
    "Find flight recommendations and a wedding venue for a trip from "
    "New York to London from September 1st to September 15th. "
    "The preferred genre of music for the playlist is grunge. "
    "No follow up questions. This is a hypothetical scenario."
)

SCORE_KEYWORDS = {
    "flight": 1,
    "venue": 1,
    "playlist": 1,
    "grunge": 1,
    "london": 1,
}

def score_response(text: str) -> int:
    text_lower = text.lower()
    return sum(v for k, v in SCORE_KEYWORDS.items() if k in text_lower)

def run_variant(system_prompt: str) -> str:
    agent = create_agent(
        model="gpt-5-nano",
        tools=[call_subagent_1, call_subagent_2, call_subagent_3],
        system_prompt=system_prompt,
    )
    result = agent.invoke({"messages": [HumanMessage(content=QUESTION)]})
    return result["messages"][-1].content


def test_prompt_variants():
    config_path = Path("tests/prompt_variants.json")
    config = json.loads(config_path.read_text())
    variants = config["variants"]
    min_score = config["min_passing_score"]

    scores = {}
    for variant in variants:
        response = run_variant(variant["system_prompt"])
        s = score_response(response)
        scores[variant["id"]] = s
        print(f"\n{'='*50}")
        print(f"Variant: {variant['id']}  |  Score: {s}/{len(SCORE_KEYWORDS)}")
        print(response[:300] + "...")

    best = max(scores, key=lambda k: scores.get(k, 0))
    print(f"\n🏆 Best variant: {best} (score={scores[best]})")

    # Fail the build if no variant clears the minimum threshold
    assert max(scores.values()) >= min_score, (
        f"No variant scored ≥{min_score}. Scores: {scores}. "
        "All prompt variants underperform the minimum quality bar."
    )