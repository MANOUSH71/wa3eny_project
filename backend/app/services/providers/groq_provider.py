import json
from groq import Groq

from app.core.config import settings
from app.models.scenario import ScenarioResponse, Difficulty
from app.services.prompts import build_scenario_prompt


class GroqProvider:

    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY) if settings.GROQ_API_KEY else None

    def generate(self, label: str, difficulty: Difficulty) -> ScenarioResponse:
        if not self.client:
            raise Exception("Groq API key not configured")

        prompt = build_scenario_prompt(label, difficulty.value)

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.7,
            max_tokens=1800,
        )

        text = response.choices[0].message.content.strip()
        text = text.replace("```json", "").replace("```", "").strip()

        start = text.find("{")
        end = text.rfind("}")

        if start >= 0 and end > start:
            text = text[start:end + 1]

        data = json.loads(text)
        return ScenarioResponse(**data)