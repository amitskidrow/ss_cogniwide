class FallbackAgent:
    """Fallback for unknown intents (simulated live agent)."""

    async def handle(self, session_id: int, text: str, locale: str):
        return "I'm sorry, I didn't understand that. A human agent will follow up soon."