from fastapi import FastAPI, Response
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

@app.api_route(
    "/health", 
    methods=["GET", "HEAD"], 
    include_in_schema=False
)
async def health():
    """
    Health check endpoint that works for uptime tools.
    Responds to both GET and HEAD requests.
    """
    return Response(content="ok", media_type="text/plain")
