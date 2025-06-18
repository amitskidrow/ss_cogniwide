import re

class IntentClassifierAgent:
    """Simple intent classifier with keyword fallback."""

    def __init__(self):
        self.intents = {
            "FAQ": ["hours", "password", "tickets", "help", "how", "what"],
            "COMPLAINT": ["complaint", "issue", "error", "bug", "problem"],
            "ACCOUNT": ["account", "billing", "subscription", "login"],
        }

    async def classify(self, text: str) -> str:
        text_lower = text.lower()
        for intent, keywords in self.intents.items():
            for kw in keywords:
                if re.search(rf"\b{re.escape(kw)}\b", text_lower):
                    return intent
        return "UNKNOWN"