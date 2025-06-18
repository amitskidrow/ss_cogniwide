import os

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    database_url: str = Field(default="sqlite+aiosqlite:///./data.db", env="DATABASE_URL")
    api_key: str = Field(..., env="API_KEY")
    sendgrid_api_key: str = Field(default=None, env="SENDGRID_API_KEY")
    twilio_account_sid: str = Field(default=None, env="TWILIO_ACCOUNT_SID")
    twilio_auth_token: str = Field(default=None, env="TWILIO_AUTH_TOKEN")

    class Config:
        case_sensitive = False
        env_file = ".env"


settings = Settings()