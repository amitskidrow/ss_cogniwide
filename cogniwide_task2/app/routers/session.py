from fastapi import APIRouter, Depends, Header, HTTPException

from app.core.config import settings
from app.db.database import database, sessions, messages, tickets, notifications

router = APIRouter(prefix="/session", tags=["session"])


async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")


@router.get("/{session_id}")
async def get_session(session_id: int, api_key: None = Depends(verify_api_key)):
    msgs = await database.fetch_all(
        messages.select().where(messages.c.session_id == session_id)
    )
    return [{"sender": m["sender"], "text": m["text"], "ts": m["ts"]} for m in msgs]


@router.delete("/{session_id}")
async def delete_session(session_id: int, api_key: None = Depends(verify_api_key)):
    await database.execute(messages.delete().where(messages.c.session_id == session_id))
    await database.execute(tickets.delete().where(tickets.c.session_id == session_id))
    await database.execute(sessions.delete().where(sessions.c.id == session_id))
    return {"deleted_session": session_id}