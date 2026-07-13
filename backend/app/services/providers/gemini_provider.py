import json
from google import genai

from app.core.config import settings
from app.models.scenario import ScenarioResponse, Difficulty
from app.services.prompts import build_scenario_prompt


class GeminiProvider:

    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY) if settings.GEMINI_API_KEY else None

    def generate(self, label: str, difficulty: Difficulty) -> ScenarioResponse:
        if not self.client:
            raise Exception("Gemini API key not configured")

        prompt = build_scenario_prompt(label, difficulty.value)

        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )

        text = response.text.strip()
        text = text.replace("```json", "").replace("```", "").strip()

        start = text.find("{")
        end = text.rfind("}")

        if start >= 0 and end > start:
            text = text[start:end + 1]

        data = json.loads(text)
        return ScenarioResponse(**data)