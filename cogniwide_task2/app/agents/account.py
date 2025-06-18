import asyncio

class AccountAgent:
    """Mock account lookup/update agent."""

    async def handle(self, session_id: int, text: str, locale: str):
        await asyncio.sleep(0.1)
        return "Your account number ****1234 is active and in good standing."