# Cogniwide AI Demo – Voice & Chat PoCs

Proof-of-concept repository showcasing two independent AI customer-support systems:

| Folder | PoC | Stack Highlights |
|--------|-----|------------------|
| `cogniwide_task1` | **AI Voice Agent System** | FastAPI · Twilio Voice / Vapi · Whisper / ElevenLabs · PostgreSQL |
| `cogniwide_task2` | **AI Multi-Agent Chat Support System** | FastAPI · OpenAI GPT-4o-mini · Vector search · SendGrid / WhatsApp · PostgreSQL |

## Repo layout

````
.
├── cogniwide_task1/      # PoC-1 voice assistant
├── cogniwide_task2/      # PoC-2 chat assistant
├── README.md             # <— you are here
└── LICENSE               # MIT
````

## Quick start (Docker)
```bash
# clone & cd
git clone https://github.com/amitskidrow/ss_cogniwide.git
cd ss_cogniwide

# PoC-1
cp cogniwide_task1/.env.example cogniwide_task1/.env
docker compose -f cogniwide_task1/docker-compose.yml up --build

# PoC-2
cp cogniwide_task2/.env.example cogniwide_task2/.env
docker compose -f cogniwide_task2/docker-compose.yml up --build
```

## Documentation

* **PoC-1 details →** [`cogniwide_task1/README.md`](cogniwide_task1/README.md)
* **PoC-2 details →** [`cogniwide_task2/README.md`](cogniwide_task2/README.md)

---

© 2025 Amit Kumar – MIT License

