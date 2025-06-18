import datetime

from app.db.database import database, tickets

class TicketAgent:
    """Creates support tickets."""

    async def handle(self, session_id: int, text: str, locale: str):
        now = datetime.datetime.utcnow()
        query = tickets.insert().values(
            session_id=session_id,
            category="COMPLAINT",
            status="OPEN",
            created_ts=now,
            resolved_ts=None,
        )
        ticket_id = await database.execute(query)
        reply = f"Your ticket number is {ticket_id}."
        return {"reply": reply, "ticket_id": ticket_id}