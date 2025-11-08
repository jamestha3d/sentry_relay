# 🧩 Sentry → Slack Relay (FastAPI)

A microservice that securely receives Sentry webhook alerts and relays them to Slack using Block Kit formatting.

## 🚀 Features
- ✅ HMAC signature verification (secure)
- 💬 Beautiful Slack messages (Block Kit)
- 🧱 Clean modular architecture
- 🆓 Works on Render free tier

## 🛠 Setup

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 🧩 Environment (.env)
```
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/XXXX/YYYY/ZZZZ
SENTRY_WEBHOOK_SECRET=your_sentry_secret
PORT=8000
ENV=development
```
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

RENDER james@tangitex.ng
BUILD command: pip install --upgrade pip pip install -r requirements.txt
START command: uvicorn app.main:app --host 0.0.0.0 --port $PORT # PORT set automatically by render, not hardcoding