from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    slack_webhook_url: str
    sentry_webhook_secret: str
    env: str = "development"
    port: int = 8000

    class Config:
        env_file = ".env"

settings = Settings()
