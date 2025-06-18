import sqlalchemy
from databases import Database

from app.core.config import settings

DATABASE_URL = settings.database_url

database = Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

sessions = sqlalchemy.Table(
    "sessions",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.String(64)),
    sqlalchemy.Column("started_ts", sqlalchemy.DateTime),
    sqlalchemy.Column("last_ts", sqlalchemy.DateTime),
    sqlalchemy.Column("status", sqlalchemy.String(16), default="OPEN"),
)

messages = sqlalchemy.Table(
    "messages",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("session_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("sessions.id")),
    sqlalchemy.Column("sender", sqlalchemy.String(16)),
    sqlalchemy.Column("text", sqlalchemy.Text),
    sqlalchemy.Column("ts", sqlalchemy.DateTime),
)

tickets = sqlalchemy.Table(
    "tickets",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("session_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("sessions.id")),
    sqlalchemy.Column("category", sqlalchemy.String(100)),
    sqlalchemy.Column("status", sqlalchemy.String(16), default="OPEN"),
    sqlalchemy.Column("created_ts", sqlalchemy.DateTime),
    sqlalchemy.Column("resolved_ts", sqlalchemy.DateTime, nullable=True),
)

notifications = sqlalchemy.Table(
    "notifications",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("ticket_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("tickets.id")),
    sqlalchemy.Column("channel", sqlalchemy.String(16)),
    sqlalchemy.Column("target", sqlalchemy.String(100)),
    sqlalchemy.Column("ts", sqlalchemy.DateTime),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL.replace("asyncpg", "psycopg2"), connect_args={"check_same_thread": False}
    if DATABASE_URL.startswith("sqlite")
    else {},
)