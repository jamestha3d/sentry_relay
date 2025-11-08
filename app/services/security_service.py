import hmac
import hashlib
from fastapi import HTTPException, Request, status
from app.core.config import settings

class SecurityService:
    @staticmethod
    async def verify_sentry_signature(request: Request):
        raw_body = await request.body()
        received_signature = request.headers.get("sentry-hook-signature")

        if not received_signature:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing Sentry signature header."
            )

        expected_signature = hmac.new(
            key=settings.sentry_webhook_secret.encode("utf-8"),
            msg=raw_body,
            digestmod=hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(expected_signature, received_signature):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Sentry signature."
            )
