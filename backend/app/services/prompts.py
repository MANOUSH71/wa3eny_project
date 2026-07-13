import random
last_channel_index = {}

def choose_channel(label: str) -> str:
    channel_options = {
        "Accounting": ["email", "whatsapp", "login_page"],
        "Human Resources": ["email", "whatsapp", "login_page"],
        "IT": ["login_page", "email", "whatsapp"],
        "Marketing": ["whatsapp", "login_page", "email"],
        "Sales": ["whatsapp", "email", "login_page"],
    }

    options = channel_options.get(label, ["email", "whatsapp", "login_page"])

    current_index = last_channel_index.get(label, -1)
    next_index = (current_index + 1) % len(options)
    last_channel_index[label] = next_index

    return options[next_index]


def build_scenario_prompt(label: str, difficulty: str) -> str:
    channel = choose_channel(label)

    department_guidance = {
        "Accounting": """
Focus on finance-related threats:
- invoice fraud
- fake vendor payment
- CEO fraud
- bank account change scams
- payroll payment manipulation
""",
        "Human Resources": """
Focus on HR-related threats:
- fake CV attachments
- fake employee benefits portal
- payroll update scams
- fake interview links
- employee credential phishing
""",
        "IT": """
Focus on IT-related threats:
- password reset phishing
- MFA fatigue
- fake admin login pages
- VPN access alerts
- fake security notifications
""",
        "Marketing": """
Focus on marketing-related threats:
- fake brand collaboration
- social media account verification
- fake shared campaign files
- fake advertising platform login
- fake influencer partnerships
""",
        "Sales": """
Focus on sales-related threats:
- fake purchase orders
- fake customer inquiries
- urgent contract review
- suspicious attachments
- fake CRM login
""",
    }

    guidance = department_guidance.get(label, department_guidance["Accounting"])

    return f"""
You are Wa3eny AI Scenario Generator for cybersecurity awareness training.

Generate a SAFE educational phishing-awareness simulation.
Do NOT include real hacking steps, malware code, credential theft instructions, or executable attack guidance.

Role or department: {label}
Difficulty: {difficulty}
Required channel: {channel}

Department-specific guidance:
{guidance}

Return ONLY valid JSON with this exact schema:
{{
  "channel": "{channel}",
  "sender_name": "...",
  "sender_handle": "...",
  "title": "...",
  "message": "...",
  "is_phishing": true,
  "red_flags": ["...", "..."],
  "questions": [
    {{
      "question": "...",
      "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
      "correct_answer": "A) Full correct option text",
      "explanation": "..."
    }},
    {{
      "question": "...",
      "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
      "correct_answer": "A) Full correct option text",
      "explanation": "..."
    }},
    {{
      "question": "...",
      "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
      "correct_answer": "A) Full correct option text",
      "explanation": "..."
    }}
  ],
  "correct_action": "...",
  "explanation": "..."
}}

Rules:
- The channel MUST be exactly: {channel}.
- Create exactly 3 questions.
- Each question must have exactly 4 options.
- correct_answer must be the full option text exactly as written in options.
- Do not return only "A", "B", "C", or "D".
- If channel is email, generate a realistic phishing email.
- If channel is whatsapp, generate a short WhatsApp-style message.
- If channel is login_page, describe the fake login page prompt shown to the user.
- Keep message under 120 words.
- Make it realistic but safe.
- Match the department and difficulty.
- sender_handle must match the channel:
  email -> fictional email address
  whatsapp -> fictional phone number
  login_page -> fictional login domain
- If is_phishing=false, red_flags must be [].
- Return ONLY the JSON object.
"""