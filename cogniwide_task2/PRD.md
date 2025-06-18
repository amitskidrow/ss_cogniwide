# PRD — AI Multi-Agent Chat Support System (PoC-2)

## 1 ▪ Purpose & Background
Create a proof-of-concept chat platform that orchestrates multiple specialised AI agents (intent classifier, router, FAQ, ticketing, account, notification) to automate most customer-support queries over a Web/API channel. The PoC validates agent architecture, latency, accuracy, and operating cost ahead of a full-scale deployment. :contentReference[oaicite:0]{index=0}

## 2 ▪ Goals & Success Metrics
| Goal | KPI / Acceptance Criteria |
|------|---------------------------|
| Accurate intent detection | ≥ 90 % top-1 intent accuracy (English baseline) |
| Autonomous resolution | ≥ 70 % chats fully handled without human escalation |
| Low latency | First agent response ≤ 2 s round-trip |
| Rapid prototyping | Fresh dev setup `docker compose up` in < 10 min |
| Agent modularity | New agent type pluggable via 1 interface & config file |

## 3 ▪ Scope
### In-Scope
* **Chat ingestion** over REST+/socket endpoint, JSON payload.  
* IntentClassifierAgent → RoutingAgent → specialised **SupportAgents** (FAQ, Ticket, Account). :contentReference[oaicite:1]{index=1}  
* NotifyAgent sending email / WhatsApp updates via Twilio SendGrid APIs. :contentReference[oaicite:2]{index=2}  
* FastAPI backend, async handling, SQLite→PostgreSQL storage, OpenAI prompt logic.  
* Minimal Swagger UI and simple HTML chat tester.

### Out-of-Scope
* Omnichannel (voice/SMS) integration—covered in PoC-1.  
* Production-grade CRM integration (stub only).  
* Advanced analytics dashboards (basic Prometheus metrics only).

## 4 ▪ User Personas
| Persona | Needs | Pain Points Addressed |
|---------|-------|-----------------------|
| Customer | Quick, correct answers 24×7 | Slow agent replies, repeated questions |
| Support Manager | Reduce ticket load & cost | High staffing costs, inconsistent answers |
| Developer Ops | Easy deploy & monitor | Complex ML stacks, unclear logs |

## 5 ▪ Functional Requirements
1. **Chat Reception**  
   * `POST /chat/message` with `user_id`, `text`, `locale`.  
   * Persist message, create session if new.  

2. **Intent Classification**  
   * OpenAI GPT-4o-mini or keyword fallback; returns `FAQ`, `COMPLAINT`, `ACCOUNT`, `UNKNOWN`. :contentReference[oaicite:3]{index=3}  

3. **Routing**  
   * RoutingAgent forwards payload to proper SupportAgent.  
   * Unknown intents escalated to `FallbackAgent` (optional live-agent simulator).

4. **Support Agents**  
   * **FAQAgent**: vector search over FAQ store → answer.  
   * **TicketAgent**: create row in `tickets` table; return ticket # in reply.  
   * **AccountAgent**: mock lookup/update; returns masked data.

5. **Notification**  
   * NotifyAgent emails/WhatsApps ticket confirmations & resolution updates.  

6. **Logging & Analytics**  
   * Tables: `messages`, `sessions`, `tickets`, `notifications`.  
   * Expose `/metrics` for Prometheus; structured JSON logs.

## 6 ▪ Non-Functional Requirements
* **Performance** — ≤ 200 ms internal processing per agent hop.  
* **Reliability** — 99 % uptime during PoC window; idempotent retries.  
* **Scalability** — Design for 100 concurrent sessions (PoC) with path to 1 k.  
* **Security** — OAuth2 token on API, env-based secrets, GDPR delete endpoint.  
* **Observability** — OpenTelemetry tracing; log correlation IDs.

## 7 ▪ Technical Architecture
```

Browser / Client ──► FastAPI `/chat/message`
│
┌─────────▼─────────┐
│ IntentClassifier  │
└─────────┬─────────┘
▼
RoutingAgent
┌───────────────┬───────────────┬───────────────┐
▼               ▼               ▼               ▼
FAQAgent     TicketAgent     AccountAgent   FallbackAgent
│               │               │               │
└──► NotifyAgent (email/WhatsApp async queue) ◄──┘
│
▼
PostgreSQL

````

| Component | Tech Stack |
|-----------|------------|
| Backend   | Python 3.11, FastAPI, Uvicorn, AsyncIO |
| LLM / NLU | OpenAI chat-completion (gpt-4o-mini) |
| Vector DB | Chroma / SQLite FTS (for FAQ) |
| Storage   | SQLite (local) → PostgreSQL (cloud) |
| Messaging | Twilio SendGrid (email) + WhatsApp Cloud API |
| Infra     | Docker Compose; optional Render deployment |

## 8 ▪ API Endpoints (draft)
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/chat/message` | Ingest user chat message |
| GET  | `/session/{id}` | Retrieve full conversation |
| GET  | `/ticket/{id}` | Fetch ticket status |
| POST | `/notify/test` | Send test notification |
| GET  | `/health` | Liveness/readiness probe |

## 9 ▪ Data Schema (simplified)
```sql
CREATE TABLE sessions (
  id SERIAL PRIMARY KEY,
  user_id VARCHAR(64),
  started_ts TIMESTAMP,
  last_ts TIMESTAMP,
  status ENUM('OPEN','CLOSED') DEFAULT 'OPEN'
);

CREATE TABLE messages (
  id SERIAL PRIMARY KEY,
  session_id INT REFERENCES sessions(id),
  sender ENUM('USER','AGENT'),
  text TEXT,
  ts TIMESTAMP
);

CREATE TABLE tickets (
  id SERIAL PRIMARY KEY,
  session_id INT REFERENCES sessions(id),
  category VARCHAR(100),
  status ENUM('OPEN','RESOLVED','ESCALATED') DEFAULT 'OPEN',
  created_ts TIMESTAMP,
  resolved_ts TIMESTAMP
);

CREATE TABLE notifications (
  id SERIAL PRIMARY KEY,
  ticket_id INT REFERENCES tickets(id),
  channel ENUM('EMAIL','WHATSAPP'),
  target VARCHAR(100),
  ts TIMESTAMP
);
````

## 10 ▪ Milestones & Timeline (4-week PoC)

| Week | Deliverable                                                      |
| ---- | ---------------------------------------------------------------- |
| 1    | FastAPI skeleton, message ingestion, sessions DB                 |
| 2    | IntentClassifierAgent + RoutingAgent, FAQAgent MVP               |
| 3    | TicketAgent, AccountAgent mocks, NotifyAgent, Prometheus metrics |
| 4    | Vector search for FAQ, Dockerfile/Compose, README, demo video    |

## 11 ▪ Risks & Mitigations

| Risk                     | Impact         | Mitigation                           |
| ------------------------ | -------------- | ------------------------------------ |
| Incorrect intent routing | Poor CX        | Confidence threshold; fallback agent |
| LLM cost spikes          | Budget overrun | Token budgeting, caching             |
| Data privacy (PII)       | Compliance     | Mask sensitive fields, GDPR delete   |

## 12 ▪ Open Questions

1. Expected peak concurrent chat sessions?
2. Language support beyond English during PoC?
3. Preferred notification channels (email only vs email + WhatsApp)?
4. Any existing FAQ or ticketing DB to integrate?
5. SLA / uptime target for PoC demo?
