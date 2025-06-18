import datetime

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from twilio.rest import Client as TwilioClient

from app.core.config import settings
from app.db.database import database, notifications

class NotifyAgent:
    """Sends notifications via email or WhatsApp and logs them."""

    async def handle(self, ticket_id: int, channel: str, target: str):
        now = datetime.datetime.utcnow()
        query = notifications.insert().values(
            ticket_id=ticket_id, channel=channel, target=target, ts=now
        )
        await database.execute(query)
        if channel.upper() == "EMAIL" and settings.sendgrid_api_key:
            message = Mail(
                from_email="support@example.com",
                to_emails=target,
                subject=f"Ticket {ticket_id} Update",
                plain_text_content=f"Your ticket {ticket_id} has been created.",
            )
            sg = SendGridAPIClient(settings.sendgrid_api_key)
            sg.send(message)
        if channel.upper() == "WHATSAPP" and settings.twilio_account_sid and settings.twilio_auth_token:
            tw_client = TwilioClient(settings.twilio_account_sid, settings.twilio_auth_token)
            tw_client.messages.create(
                from_="whatsapp:+14155238886",
                to=f"whatsapp:{target}",
                body=f"Your ticket {ticket_id} has been created.",
            )