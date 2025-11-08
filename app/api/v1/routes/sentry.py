from fastapi import APIRouter, Request, BackgroundTasks
from app.services.sentry_service import SentryService
from app.services.security_service import SecurityService

router = APIRouter()

@router.post("/webhook/sentry", status_code=202)
async def sentry_webhook(request: Request, background_tasks: BackgroundTasks):
    await SecurityService.verify_sentry_signature(request)
    payload = await request.json()
    background_tasks.add_task(SentryService.process_event, payload)
    return {"detail": "Sentry event received and will be processed."}
