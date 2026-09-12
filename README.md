# Agentic AI Customer Support

A portfolio-ready customer-support application using:

- React + Vite frontend
- FastAPI backend
- LangGraph agent
- RAG knowledge retrieval
- Business tools for order/refund/cancellation
- PostgreSQL-ready database layer
- Docker support

## 1. Backend

```bash
cd backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your OpenAI API key.

Run:

```bash
uvicorn app:app --reload
```

Backend:
http://localhost:8000

## 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal.

If the backend is deployed, create:

```text
VITE_API_URL=https://your-backend-url
```

in the frontend deployment environment.

## Demo order IDs

- 1001 = shipped
- 1002 = delayed
- 1003 = delivered

Try:

- "Where is order #1001?"
- "My order #1002 is late"
- "I want a refund for order #1003"
- "Cancel order #1001"

## Production upgrades

For a real production system, add:
- JWT/OAuth authentication
- real order/payment APIs
- persistent conversation history
- a real vector database
- document ingestion pipeline
- human-agent dashboard
- structured logging
- rate limiting
- secrets management
- monitoring and tests
