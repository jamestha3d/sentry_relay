import textwrap
import httpx
from app.core.config import settings
import os
import logging
import traceback

class SlackService:
    @staticmethod
    def build_sentry_message(payload: dict) -> dict:
        """
        Build a detailed Slack Block Kit message from a Sentry webhook payload.
        """
        event = payload.get("data", {}).get("event", {})
        project = payload.get("project", {}).get("slug", "unknown-project")

        title = event.get("title", "No title")
        culprit = event.get("culprit", "Unknown culprit")
        environment = event.get("environment", "Unknown")
        url = event.get("url", "")
        exception_values = event.get("exception", {}).get("values", [])

        # Extract first exception if available
        exc_type = exc_value = "N/A"
        stacktrace_text = "No stacktrace available"
        if exception_values:
            first_exc = exception_values[0]
            exc_type = first_exc.get("type", "N/A")
            exc_value = first_exc.get("value", "N/A")

            frames = first_exc.get("stacktrace", {}).get("frames", [])

            # Capture both the start and end of the stacktrace for better context
            displayed_frames = []
            if len(frames) > 12:
                displayed_frames = frames[:5] + [{"filename": "...", "function": "...", "lineno": "..."}] + frames[-5:]
            else:
                displayed_frames = frames

            # Format frames into aligned readable lines
            formatted_frames = [
                f"{f.get('filename', '?')}:{f.get('lineno', '?')} → {f.get('function', '?')}"
                for f in displayed_frames
            ]

            # Indent the stack trace for Slack’s code block formatting
            stacktrace_text = textwrap.indent("\n".join(formatted_frames), prefix="    ")

        # Compose Slack message with detailed data
        return {
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f":rotating_light: New Error in {project}"
                    },
                },
                {
                    "type": "section",
                    "fields": [
                        {"type": "mrkdwn", "text": f"*Title:*\n{title}"},
                        {"type": "mrkdwn", "text": f"*Culprit:*\n{culprit}"},
                        {"type": "mrkdwn", "text": f"*Environment:*\n{environment}"},
                        {"type": "mrkdwn", "text": f"*Exception:*\n{exc_type}: {exc_value}"},
                    ],
                },
                {"type": "divider"},
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Stacktrace:*\n```{stacktrace_text}```"
                    },
                },
                {"type": "divider"},
                {
                    "type": "context",
                    "elements": [
                        {"type": "mrkdwn", "text": f"<{url}|View full details in Sentry>"},
                        {"type": "mrkdwn", "text": ":satellite_antenna: *Sentry Relay Service*"},
                    ],
                },
            ]
        }
    
    @staticmethod
    async def send_message(payload):
        blocks = SlackService.build_sentry_message(payload)

        async with httpx.AsyncClient() as client:
            response = await client.post(
                settings.slack_webhook_url, json=blocks
            )
            response.raise_for_status()
