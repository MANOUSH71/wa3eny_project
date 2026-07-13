from app.models.scenario import ScenarioResponse, Difficulty

from app.services.providers.groq_provider import GroqProvider
from app.services.providers.gemini_provider import GeminiProvider
from app.services.scenario_bank import ScenarioBank

DEPARTMENTS = {
    "accounting": "Accounting",
    "hr": "Human Resources",
    "it": "IT",
    "marketing": "Marketing",
    "sales": "Sales",
}

SECTORS = {
    "banking": "Banking & Transfers",
    "shopping": "Online Shopping",
    "social": "Social Media",
}

groq = GroqProvider()
gemini = GeminiProvider()


async def generate_scenario(
    label: str,
    difficulty: Difficulty,
) -> ScenarioResponse:
    """
    AI Orchestrator

    Priority:
    1. Groq
    2. Gemini
    3. Scenario Bank
    """

    # Try Groq
    try:
        print("Trying Groq...")
        return groq.generate(label, difficulty)

    except Exception as e:
        print(f"Groq failed: {e}")

    # Try Gemini
    try:
        print("Trying Gemini...")
        return gemini.generate(label, difficulty)

    except Exception as e:
        print(f"Gemini failed: {e}")

    # Final fallback
    print("Using Scenario Bank...")

    return ScenarioBank.get_scenario(label, difficulty)