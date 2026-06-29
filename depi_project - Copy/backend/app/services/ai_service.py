import anthropic
import json
from app.core.config import settings
from app.models.scenario import ScenarioResponse, Difficulty

client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY) if settings.ANTHROPIC_API_KEY else None

DEPARTMENTS = {
    'accounting': 'Accounting',
    'hr': 'Human Resources',
    'it': 'IT',
    'marketing': 'Marketing',
    'sales': 'Sales'
}

SECTORS = {
    'banking': 'Banking & Transfers',
    'shopping': 'Online Shopping',
    'social': 'Social Media'
}

async def generate_scenario(label: str, difficulty: Difficulty) -> ScenarioResponse:
    """Generate AI-powered phishing scenario using Claude"""
    
    if not client:
        raise Exception("Anthropic API key not configured")
    
    system_prompt = """You are a scenario-generation engine for cybersecurity training. Return ONLY valid JSON:
{"channel":"email|whatsapp|login_page","sender_name":"...","sender_handle":"...","title":"...","message":"...","is_phishing":true|false,"red_flags":["..."],"correct_action":"...","explanation":"..."}

60% phishing, 40% safe. Keep message under 100 words. red_flags=[] when is_phishing=false."""

    user_message = f"Role: {label}\nDifficulty: {difficulty.value}\nGenerate scenario."

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}]
    )
    
    text = message.content[0].text.strip().replace('```json', '').replace('```', '').strip()
    start, end = text.find('{'), text.rfind('}')
    if start >= 0 and end > start:
        text = text[start:end+1]
    
    return ScenarioResponse(**json.loads(text))
