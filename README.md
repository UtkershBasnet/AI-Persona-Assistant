# AI Persona Assistant

An AI-powered portfolio assistant for Utkersh Basnet. Ask about his experience and projects, book interviews through Cal.com, and interact via web chat or a phone call — all grounded in his real resume and GitHub repos.

**Live links**
- Chat UI: https://ai-persona.vercel.app
- Backend API: https://ai-persona.onrender.com
- Voice: +16626415534, https://vapi.ai?demo=true&shareKey=b812c7df-ee34-4a17-806b-6c807db4028f&assistantId=99fe09d3-bc2c-46d3-aaf9-f2bffee9cc3b

---

## What it does

| Capability | How |
|---|---|
| Answers questions about background, skills, projects | RAG over resume + GitHub markdown |
| Discusses any GitHub repo — tech, purpose, tradeoffs | Per-repo context files in `data/github/` |
| Books interviews end-to-end | Cal.com API — no redirect, fully automated |
| Handles voice calls | Vapi + custom LLM endpoint → Groq |
| Stays honest on edge cases | Grounded retrieval, no hallucination fallback |

---

## Architecture

### High-level overview

```
┌─────────────────┐     ┌──────────────────────────────────────────┐
│   Next.js UI    │────▶│              FastAPI Backend               │
│   (Vercel)      │     │              (Render)                      │
└─────────────────┘     │                                            │
                        │  ┌─────────────┐    ┌──────────────────┐  │
┌─────────────────┐     │  │ RAG Pipeline │    │  Cal.com API     │  │
│   Vapi Voice    │────▶│  │ ChromaDB +  │    │  Booking engine  │  │
│   (phone call)  │     │  │ Gemini embed│    └──────────────────┘  │
└─────────────────┘     │  └──────┬──────┘                          │
                        │         │ retrieved chunks                 │
                        │  ┌──────▼──────┐                          │
                        │  │  Groq LLM   │                          │
                        │  │ (generation)│                          │
                        │  └─────────────┘                          │
                        └──────────────────────────────────────────┘
```

### Chat request flow

```
User types message
      │
      ▼
POST /api/chat/
      │
      ▼
ChromaDB similarity search (top 6 chunks)
      │
      ▼
Chunks injected into system prompt
      │
      ▼
Groq llama-3.3-70b-versatile generates response
      │
      ├── contains [BOOK_MEETING] tag?
      │         │
      │         ▼ yes
      │   Validate date/time (IST → UTC)
      │   POST to Cal.com /v2/bookings
      │   Return booking confirmation
      │
      ▼ no
Return grounded response to frontend
```

### Voice request flow

```
Caller dials Twilio number
      │
      ▼
Vapi handles STT (Deepgram Nova 3)
      │
      ▼
POST /api/vapi/chat/completions   ← OpenAI-compatible format
      │
      ▼
ChromaDB similarity search (top 4 chunks, faster)
      │
      ▼
Voice-optimised prompt (2–4 sentences max)
      │
      ▼
Groq llama-3.1-8b-instant (lowest latency)
      │
      ├── [BOOK_MEETING] tag detected?
      │         │
      │         ▼ yes
      │   Strip tag from spoken output
      │   Fire Cal.com booking in background
      │
      ▼
SSE stream back to Vapi → TTS → Caller hears response
```

First-response latency target: **< 2 seconds**

---

## Stack

| Layer | Technology | Why |
|---|---|---|
| Frontend | Next.js on Vercel | Zero-config deployment, free tier |
| Backend | FastAPI on Render | Async, fast startup, free tier |
| Embeddings | Gemini `embedding-001` | Better semantic quality than local models |
| Vector DB | ChromaDB (local) | No hosted DB needed, committed to git |
| LLM (chat) | Groq `llama-3.3-70b-versatile` | Best open-source quality |
| LLM (voice) | Groq `llama-3.1-8b-instant` | Lowest latency for < 2s voice target |
| Voice orchestration | Vapi | Handles telephony, STT, TTS |
| STT | Deepgram Nova 3 (via Vapi) | Fast, accurate |
| Calendar | Cal.com API v2 | Real slot fetch + booking, no redirect |
| Telephony | Twilio (free trial) | Phone number for inbound calls |

---

## Project layout

```
ai-persona/
├── backend/
│   ├── api/
│   │   ├── chat.py          # web chat endpoint
│   │   ├── calendar.py      # slot fetch + booking
│   │   └── vapi.py          # Vapi-compatible voice endpoint
│   ├── rag/
│   │   ├── chain.py         # prompt construction + LLM call
│   │   ├── embeddings.py    # Gemini embedding wrapper
│   │   ├── loader.py        # markdown chunking
│   │   ├── runtime.py       # lazy Chroma initialisation
│   │   └── vectorstore.py   # Chroma load/save
│   ├── scripts/
│   │   ├── ingest.py        # build the vector index
│   │   └── setup_vapi.py    # create Vapi assistant via API
│   ├── config.py
│   └── main.py
├── chroma_db/               # committed to git — pre-built index
├── data/
│   ├── resume.md
│   ├── github_context.md
│   └── github/              # one .md per repo
├── frontend/                # Next.js app
├── voice/
│   └── vapi_config.json     # exported assistant config
├── .env.example
├── Procfile
└── requirements.txt
```

---

## Local setup

### 1. Clone and install

```bash
git clone https://github.com/utkershbasnet/ai-persona.git
cd ai-persona

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cd frontend && npm install && cd ..
```

### 2. Configure environment

```bash
cp .env.example .env
# fill in your keys — see Environment variables below
```

### 3. Build the Chroma index

Only needed if you change `data/` or the embedding model. The committed `chroma_db/` is ready to use out of the box.

```bash
source venv/bin/activate
python -m backend.scripts.ingest
```

### 4. Start backend

```bash
source venv/bin/activate
uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

### 5. Start frontend

```bash
cd frontend
npm run dev
```

Open:
- Frontend: http://localhost:3000
- API docs: http://127.0.0.1:8000/docs

---

## Environment variables

Copy `.env.example` to `.env` and fill in:

```bash
# LLM
GROQ_API_KEY=

# Embeddings
GOOGLE_API_KEY=

# Calendar
CAL_COM_API_KEY=
CAL_COM_EVENT_TYPE_ID=
CAL_COM_LINK=

# Voice
VAPI_API_KEY=
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=

# Models (defaults shown)
CHAT_MODEL=llama-3.3-70b-versatile
VOICE_MODEL=llama-3.1-8b-instant
EMBEDDING_MODEL=models/gemini-embedding-001

# Paths (defaults shown)
CHROMA_PERSIST_DIR=./chroma_db
DATA_DIR=./data
```

---

## API reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Service status + retrieval state |
| `POST` | `/api/chat/` | Grounded persona chat |
| `POST` | `/api/chat/reset` | Clear a session |
| `GET` | `/api/calendar/slots` | Fetch real available Cal.com slots |
| `POST` | `/api/calendar/book` | Create a booking directly |
| `GET` | `/api/calendar/link` | Fallback booking link |
| `POST` | `/api/vapi/chat/completions` | Vapi-compatible voice endpoint |

---

## Deployment

### Backend → Render

- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}`
- Instance type: Free
- Add all env vars in the Render dashboard

The backend uses lazy Chroma initialisation — it binds to the port immediately and only loads the vector index on the first retrieval request. This prevents Render's port-scan timeout.

To keep the free tier warm during demo window, ping `/health` every 10 minutes via [cron-job.org](https://cron-job.org).

### Frontend → Vercel

- Root directory: `frontend`
- Framework preset: Next.js
- Environment variable: `NEXT_PUBLIC_API_URL=https://your-app.onrender.com`

### Voice → Vapi

After deploying the backend, create the Vapi assistant pointing to your live URL:

```bash
python -m backend.scripts.setup_vapi --url https://your-app.onrender.com
```

---

## Knowledge base

The assistant is grounded in three sources — no hardcoded answers:

| File | Contents |
|---|---|
| `data/resume.md` | Education, experience, skills |
| `data/github_context.md` | Combined GitHub overview |
| `data/github/*.md` | Per-repo: purpose, stack, decisions, tradeoffs |

To update knowledge: edit the markdown files, rerun `python -m backend.scripts.ingest`, commit the updated `chroma_db/`, redeploy.

---

## Key design decisions

**RAG over static prompting** — The assistant retrieves only the most relevant chunks per question rather than stuffing everything into a fixed prompt. This keeps responses accurate and the system easy to update.

**Local ChromaDB committed to git** — Avoids needing a hosted vector database. The tradeoff is that the index must be rebuilt and recommitted when source data changes, which is acceptable for a single-persona system.

**Hosted Gemini embeddings** — Outsourcing embeddings removes the need to load a heavy local ML model on Render's free tier, reducing memory pressure and cold-start time.

**Lazy Chroma initialisation** — The vectorstore loads only on the first retrieval request, not at startup. This lets the process bind to its HTTP port quickly and avoids Render's port-scan timeout.

**Separate models for chat vs voice** — `llama-3.3-70b` for chat prioritises quality; `llama-3.1-8b-instant` for voice prioritises latency. Both run on Groq's free tier.

**Vapi as a dumb pipe** — Vapi handles telephony and audio only. All retrieval and generation runs in the FastAPI backend via a custom LLM URL. This means voice and chat use the exact same RAG pipeline and produce consistent answers.

---

## Limitations

- `chroma_db/` must be rebuilt and recommitted when source data or the embedding model changes
- Conversation history is in-memory and lost on server restart
- The free Render tier spins down after inactivity — first request after idle takes ~30s
- Booking confirmation is best-effort on voice calls; failures are silent to avoid breaking the call
