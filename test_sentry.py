import hmac, hashlib, json, requests
from app.core.config import settings
WEBHOOK_URL = "http://127.0.0.1:8000/v1/webhook/sentry"
SECRET = settings.sentry_webhook_secret.encode("utf-8")

payload = {
    "data": {
        "event": {
            "title": "Test Error",
            "culprit": "views.py",
            "environment": "development"
        }
    },
    "project": {"slug": "my-test-project"}
}

body = json.dumps(payload).encode("utf-8")
signature = hmac.new(SECRET, body, hashlib.sha256).hexdigest()

headers = {
    "Content-Type": "application/json",
    "sentry-hook-signature": signature
}

response = requests.post(WEBHOOK_URL, data=body, headers=headers)

try:
    data = response.json()
except json.JSONDecodeError:
    data = {"raw_text": response.text}

print("Response:", data)
#print(response.status_code, response.json())
