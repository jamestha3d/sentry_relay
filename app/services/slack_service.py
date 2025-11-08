import httpx
from app.core.config import settings

class SlackService:
    @staticmethod
    async def send_message(title: str, project: str, culprit: str, environment: str):
        blocks = [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": f"🚨 New Error in {project}", "emoji": True}
            },
            {"type": "divider"},
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Title:*{title}"},
                    {"type": "mrkdwn", "text": f"*Culprit:*{culprit}"},
                    {"type": "mrkdwn", "text": f"*Environment:*{environment}"},
                ]
            },
            {"type": "divider"},
            {"type": "context", "elements": [{"type": "mrkdwn", "text": "📡 Sentry Alert Relay"}]}
        ]

        async with httpx.AsyncClient() as client:
            response = await client.post(
                settings.slack_webhook_url, json={"blocks": blocks}
            )
            response.raise_for_status()
