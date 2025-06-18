from fastapi import APIRouter, Depends, Header, HTTPException

from app.core.config import settings
from app.db.database import database, tickets

router = APIRouter(prefix="/ticket", tags=["ticket"])


async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")


@router.get("/{ticket_id}")
async def get_ticket(ticket_id: int, api_key: None = Depends(verify_api_key)):
    ticket = await database.fetch_one(tickets.select().where(tickets.c.id == ticket_id))
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return {
        "id": ticket["id"],
        "session_id": ticket["session_id"],
        "category": ticket["category"],
        "status": ticket["status"],
        "created_ts": ticket["created_ts"],
        "resolved_ts": ticket["resolved_ts"],
    }