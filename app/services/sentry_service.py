from app.services.slack_service import SlackService

class SentryService:
    @staticmethod
    async def process_event(payload: dict):
        # event = payload.get("data", {}).get("event", {})
        # title = event.get("title", "No title")
        # culprit = event.get("culprit", "Unknown")
        # project = payload.get("project", {}).get("slug", "Unknown project")
        # environment = event.get("environment", "N/A")

        await SlackService.send_message(payload)
