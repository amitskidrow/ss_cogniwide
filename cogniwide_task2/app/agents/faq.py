import json
import os

class FAQAgent:
    """Simple FAQ agent using static JSON store."""

    def __init__(self, faq_path: str):
        self.faq_items = []
        if os.path.exists(faq_path):
            with open(faq_path, "r", encoding="utf-8") as f:
                self.faq_items = json.load(f)

    async def handle(self, session_id: int, text: str, locale: str):
        text_lower = text.lower()
        for item in self.faq_items:
            if item["question"].lower() in text_lower:
                return item["answer"]
        return "Sorry, I couldn't find an answer in the FAQ."