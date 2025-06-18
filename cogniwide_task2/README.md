# AI Multi-Agent Chat Support System (PoC-2)

Proof-of-concept chat platform orchestrating multiple AI agents (intent classifier, router, FAQ, ticketing, account, notification).

## Requirements
- Docker & Docker Compose

## Quickstart
```bash
# Build and launch services
docker-compose up --build

# In a new terminal, send a test chat message:
curl -X POST http://localhost:8000/chat/message \
  -H "X-API-KEY: your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"user123","text":"Hello, I need help","locale":"en"}'
```

## Endpoints
- `POST /chat/message`
- `GET /session/{id}`
- `GET /ticket/{id}`
- `POST /notify/test`
- `GET /health`
- `DELETE /session/{id}`
- `/metrics` (Prometheus)

For full details see [PRD.md](PRD.md).