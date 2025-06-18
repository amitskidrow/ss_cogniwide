from fastapi import APIRouter, Depends, Header

from pydantic import BaseModel

from app.core.config import settings
from app.agents.notify import NotifyAgent

router = APIRouter(prefix="/notify", tags=["notify"])


async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != settings.api_key:
        from fastapi import HTTPException

        raise HTTPException(status_code=401, detail="Invalid API key")


class NotifyTestRequest(BaseModel):
    ticket_id: int
    channel: str
    target: str


@router.post("/test")
async def notify_test(req: NotifyTestRequest, api_key: None = Depends(verify_api_key)):
    agent = NotifyAgent()
    await agent.handle(ticket_id=req.ticket_id, channel=req.channel, target=req.target)
    return {"status": "sent", "ticket_id": req.ticket_id}