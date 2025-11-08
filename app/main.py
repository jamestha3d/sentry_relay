from fastapi import FastAPI
from app.api.v1.routes import sentry

app = FastAPI(
    title="Sentry Relay Microservice",
    version="1.1.0",
    description="Securely receives Sentry webhooks and forwards them to Slack."
)

app.include_router(sentry.router, prefix="/v1", tags=["Sentry"])

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health():
    return {"status": "ok"}
