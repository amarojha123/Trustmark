# TRUST MARK — Key-and-database setup (Windows Git Bash)

## Prerequisites
Node.js 20+, Python 3.10+, running MongoDB local or Atlas. For local Docker MongoDB: `docker compose up -d` (Docker Desktop must be running).

## One-time setup from repository root
```bash
cp backend/.env.example backend/.env
cp ai-service/.env.example ai-service/.env
cp frontend/.env.example frontend/.env
```
Fill in **backend/.env**: `MONGO_URI`, `JWT_SECRET` (at least 32 characters), `DEMO_PASSWORD`, and optionally `AI_URL` / `FRONTEND_URL` if not using localhost.
Fill in **ai-service/.env**: `GEMINI_API_KEY` and `GEMINI_MODEL` (optional; rule-only analysis works without key).
Frontend `.env` defaults to local backend.

Install and seed:
```bash
cd backend && npm install && npm run seed && cd ..
cd ai-service && python -m pip install -r requirements.txt && cd ..
cd frontend && npm install && cd ..
```

Run in three Git Bash terminals (each starting at project root):
```bash
cd ai-service && python -m uvicorn main:app --reload --port 8000
```
```bash
cd backend && npm start
```
```bash
cd frontend && npm run dev
```
Open http://localhost:5173 and sign in with creator@trustmark.local, admin@trustmark.local or manager@trustmark.local using your DEMO_PASSWORD.

## Demo
Admin saves guidelines -> Creator analyzes sample -> reviews highlighted phrases and evidence -> accepts/rejects findings -> saves and submits -> Manager approves -> Dashboard counts update. History shows changes.

## Evaluation
From `ai-service` run `python -m unittest test_retrieval.py` and `python evaluate.py` (remove GEMINI_API_KEY from environment to evaluate deterministic rules only).

## Scope and limitations
The retrieval engine uses token overlap, **not vector embeddings or true semantic RAG**. Findings are source-linked, but source authenticity and LLM interpretations require human review. The compliance score is a heuristic. This is a hackathon MVP, not a regulatory compliance certification. Evaluation uses synthetic examples, not real-world benchmark data.
