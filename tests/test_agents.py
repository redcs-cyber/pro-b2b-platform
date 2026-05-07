from jarvis.agents import GoodMoodEngine, classify_intent
from jarvis.ironman import format_ironman


def test_goodmood_changes_with_positive_text() -> None:
    engine = GoodMoodEngine()
    assert engine.observe("harika iş") == 55


def test_intent_classification() -> None:
    assert classify_intent("run notepad") == "command"
    assert classify_intent("nasılsın") == "llm"


def test_ironman_prefix() -> None:
    assert format_ironman("hazır").startswith("[JARVIS HUD]")
