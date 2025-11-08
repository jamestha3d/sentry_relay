import hmac, hashlib, json, requests

WEBHOOK_URL = "http://127.0.0.1:8000/v1/webhook/sentry"
SECRET = "your_sentry_secret_here"

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
signature = hmac.new(SECRET.encode(), body, hashlib.sha256).hexdigest()

headers = {
    "Content-Type": "application/json",
    "sentry-hook-signature": signature
}

response = requests.post(WEBHOOK_URL, data=body, headers=headers)
print(response.status_code, response.json())
