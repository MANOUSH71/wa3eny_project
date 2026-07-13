import random
from app.models.scenario import ScenarioResponse, Difficulty


class ScenarioBank:

    @staticmethod
    def get_scenario(label: str, difficulty: Difficulty) -> ScenarioResponse:
        scenarios = {
            "Accounting": [
                {
                    "sender_name": "Finance Manager",
                    "sender_handle": "finance-manager@company-training.com",
                    "title": "Urgent Invoice Payment Request",
                    "message": "Please process the attached invoice before 4 PM today.",
                    "red_flags": ["Urgency", "Payment pressure", "Unverified invoice"],
                    "correct_action": "Verify the invoice through official channels.",
                    "explanation": "Invoice fraud is one of the most common finance attacks."
                }
            ],
            "Human Resources": [
                {
                    "sender_name": "Benefits Office",
                    "sender_handle": "benefits-update@employee-portal.com",
                    "title": "Benefits Update Required",
                    "message": "Please update your employee benefits today.",
                    "red_flags": ["Fake portal", "Urgency", "Credential harvesting"],
                    "correct_action": "Access only the official HR portal.",
                    "explanation": "HR staff are commonly targeted with fake employee portals."
                }
            ],
            "IT": [
                {
                    "sender_name": "IT Security",
                    "sender_handle": "security-alert@company-support.com",
                    "title": "Password Reset Required",
                    "message": "Your password expires today. Reset it immediately.",
                    "red_flags": ["Password pressure", "Fake security domain", "Urgent action"],
                    "correct_action": "Go directly to the official portal.",
                    "explanation": "Password reset phishing is common against IT staff."
                }
            ],
            "Marketing": [
                {
                    "sender_name": "Brand Collaboration Team",
                    "sender_handle": "collab@brand-partner-offer.com",
                    "title": "Paid Collaboration Opportunity",
                    "message": "Please sign in to view the shared campaign brief for a new collaboration.",
                    "red_flags": ["Unknown sender", "Login required", "External file link"],
                    "correct_action": "Verify the sender and use trusted company platforms.",
                    "explanation": "Marketing teams are often targeted with fake collaboration offers."
                }
            ],
            "Sales": [
                {
                    "sender_name": "New Client",
                    "sender_handle": "client-request@business-order.com",
                    "title": "Urgent Purchase Order",
                    "message": "Please open the attached purchase order and confirm pricing today.",
                    "red_flags": ["Unexpected large order", "Attachment risk", "Urgent confirmation"],
                    "correct_action": "Verify the client and scan attachments before responding.",
                    "explanation": "Sales teams can be targeted with fake purchase orders."
                }
            ],
        }

        selected = random.choice(scenarios.get(label, scenarios["Accounting"]))

        return ScenarioResponse(
            channel="email",
            sender_name=selected["sender_name"],
            sender_handle=selected["sender_handle"],
            title=selected["title"],
            message=selected["message"],
            is_phishing=True,
            red_flags=selected["red_flags"],
            questions=[
                {
                    "question": "What is the biggest warning sign?",
                    "options": [
                        selected["red_flags"][0],
                        "Greeting",
                        "English language",
                        "Company signature"
                    ],
                    "correct_answer": selected["red_flags"][0],
                    "explanation": "Always investigate the primary red flag."
                },
                {
                    "question": "What should you do first?",
                    "options": [
                        selected["correct_action"],
                        "Click the link",
                        "Reply immediately",
                        "Ignore forever"
                    ],
                    "correct_answer": selected["correct_action"],
                    "explanation": "Verification is always the safest first action."
                },
                {
                    "question": "Is this suspicious?",
                    "options": [
                        "Yes",
                        "No",
                        "Not enough information",
                        "Only if sent at night"
                    ],
                    "correct_answer": "Yes",
                    "explanation": "The message contains multiple phishing indicators."
                }
            ],
            correct_action=selected["correct_action"],
            explanation=selected["explanation"]
        )