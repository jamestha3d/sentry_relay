import textwrap

class SlackService:
    @staticmethod
    def send_message(payload: dict) -> dict:
        """Format detailed Sentry webhook into a rich Slack Block Kit message."""

        event = payload.get("data", {}).get("event", {})
        project = payload.get("project", {}).get("slug", "unknown-project")

        title = event.get("title", "No title")
        culprit = event.get("culprit", "Unknown culprit")
        environment = event.get("environment", "Unknown")
        url = event.get("url", "")
        exception_values = event.get("exception", {}).get("values", [])

        # Extract first exception if present
        exc_type = exc_value = stacktrace_text = "N/A"
        if exception_values:
            first_exc = exception_values[0]
            exc_type = first_exc.get("type", "N/A")
            exc_value = first_exc.get("value", "N/A")

            frames = first_exc.get("stacktrace", {}).get("frames", [])
            # Format stacktrace into a code block for Slack
            formatted_frames = []
            for f in frames[-6:]:  # last 6 frames (avoid huge messages)
                formatted_frames.append(
                    f"{f.get('filename', '?')}:{f.get('lineno', '?')} in {f.get('function', '?')}"
                )
            stacktrace_text = "\n".join(formatted_frames) if formatted_frames else "No stacktrace"

        # Construct Slack Block Kit payload
        return {
            "blocks": [
                {
                    "type": "header",
                    "text": {"type": "plain_text", "text": f":rotating_light: New Error in {project}"}
                },
                {
                    "type": "section",
                    "fields": [
                        {"type": "mrkdwn", "text": f"*Title:*\n{title}"},
                        {"type": "mrkdwn", "text": f"*Culprit:*\n{culprit}"},
                        {"type": "mrkdwn", "text": f"*Exception:*\n{exc_type}: {exc_value}"},
                        {"type": "mrkdwn", "text": f"*Environment:*\n{environment}"},
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
                        {"type": "mrkdwn", "text": f"<{url}|View in Sentry>"},
                        {"type": "mrkdwn", "text": ":satellite_antenna: *Sentry Relay Service*"},
                    ],
                },
            ]
        }
