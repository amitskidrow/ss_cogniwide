import datetime

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel

from app.core.config import settings
from app.db.database import database, sessions, messages
from app.agents.intent import IntentClassifierAgent
from app.agents.routing import RoutingAgent
from app.agents.faq import FAQAgent
from app.agents.ticket import TicketAgent
from app.agents.account import AccountAgent
from app.agents.fallback import FallbackAgent
from app.agents.notify import NotifyAgent

router = APIRouter(tags=["chat"])


async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")


class ChatRequest(BaseModel):
    user_id: str
    text: str
    locale: str


@router.post("/chat/message")
async def chat_message(
    req: ChatRequest, api_key: None = Depends(verify_api_key)
):
    now = datetime.datetime.utcnow()
    query = sessions.select().where(
        sessions.c.user_id == req.user_id, sessions.c.status == "OPEN"
    )
    session = await database.fetch_one(query)
    if not session:
        session_data = {"user_id": req.user_id, "started_ts": now, "last_ts": now}
        sid = await database.execute(sessions.insert().values(**session_data))
        session_id = sid
    else:
        session_id = session["id"]
        await database.execute(
            sessions.update().where(sessions.c.id == session_id).values(last_ts=now)
        )

    await database.execute(
        messages.insert().values(
            session_id=session_id, sender="USER", text=req.text, ts=now
        )
    )

    intent_agent = IntentClassifierAgent()
    faq_agent = FAQAgent(faq_path="data/faq.json")
    ticket_agent = TicketAgent()
    account_agent = AccountAgent()
    fallback_agent = FallbackAgent()
    notify_agent = NotifyAgent()

    routing_agent = RoutingAgent(
        {"FAQ": faq_agent, "COMPLAINT": ticket_agent, "ACCOUNT": account_agent, "UNKNOWN": fallback_agent}
    )

    intent = await intent_agent.classify(req.text)
    result = await routing_agent.route(
        intent=intent, session_id=session_id, text=req.text, locale=req.locale
    )

    if isinstance(result, dict):
        reply = result.get("reply")
        ticket_id = result.get("ticket_id")
        if ticket_id:
            await notify_agent.handle(
                ticket_id=ticket_id, channel="EMAIL", target=req.user_id
            )
    else:
        reply = result

    now2 = datetime.datetime.utcnow()
    await database.execute(
        messages.insert().values(
            session_id=session_id, sender="AGENT", text=reply, ts=now2
        )
    )

    return {"session_id": session_id, "reply": reply}