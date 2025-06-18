class RoutingAgent:
    """Routes classified intent to the corresponding support agent."""

    def __init__(self, agents: dict):
        self.agents = agents

    async def route(self, intent: str, **kwargs):
        agent = self.agents.get(intent)
        if agent:
            return await agent.handle(**kwargs)
        fallback = self.agents.get("UNKNOWN")
        return await fallback.handle(**kwargs)