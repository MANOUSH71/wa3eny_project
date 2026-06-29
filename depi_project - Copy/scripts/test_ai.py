"""
Test Anthropic Claude API connection
"""
import os
import sys
from dotenv import load_dotenv

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

load_dotenv("backend/.env")

from app.services.ai_service import generate_scenario
from app.models.scenario import Difficulty
import asyncio

async def main():
    print("🤖 Testing Anthropic Claude API...\n")
    
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ Error: ANTHROPIC_API_KEY not set in backend/.env")
        return
    
    try:
        print("📝 Generating test scenario for Accounting department...\n")
        scenario = await generate_scenario("Accounting", Difficulty.MEDIUM)
        
        print("✅ Success! Scenario generated:\n")
        print(f"📧 Channel: {scenario.channel}")
        print(f"👤 Sender: {scenario.sender_name} <{scenario.sender_handle}>")
        print(f"📌 Title: {scenario.title}")
        print(f"💬 Message: {scenario.message[:100]}...")
        print(f"🎣 Is Phishing: {scenario.is_phishing}")
        print(f"🚩 Red Flags: {len(scenario.red_flags)}")
        
        if scenario.red_flags:
            print("\nRed Flags:")
            for flag in scenario.red_flags:
                print(f"  • {flag}")
        
        print(f"\n✅ Correct Action: {scenario.correct_action}")
        print(f"📖 Explanation: {scenario.explanation[:150]}...")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
