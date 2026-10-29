# TRUST MARK — Hackathon end-to-end starter

**Workflow:** Admin saves brand rules → Creator uploads/pastes content → rule-based + optional Gemini analysis → Creator accepts/rejects suggestions, saves and submits → Manager approves/requests revisions → Dashboard and audit history update from MongoDB.

## Prerequisites
- Windows with Node.js 20+, Python 3.10+, npm
- MongoDB Community Server **or** Docker Desktop **or** MongoDB Atlas
- Gemini API key optional. Without one, deterministic checks still work.

## ONE-TIME SETUP (VS Code PowerShell, project root)

1. Unzip and open the inner `trustmark-mvp` folder in VS Code.
2. Start MongoDB. With Docker Desktop: `docker compose up -d` (run in the project root). Or start local MongoDB Community service. Or set `MONGO_URI` to an Atlas connection URI.
3. Copy the example env files:

```powershell
Copy-Item backend/.env.example backend/.env
Copy-Item ai-service/.env.example ai-service/.env
Copy-Item frontend/.env.example frontend/.env
```

4. Edit **backend/.env**: set `MONGO_URI` (if not local), set `JWT_SECRET` to a random value, and **add** `DEMO_PASSWORD` with at least 10 characters. Generate secret with:

```powershell
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```

5. Optional: paste Gemini key in `ai-service/.env` as `GEMINI_API_KEY=...` and set `GEMINI_MODEL` to a model available to your account. If blank, only rule checks run.
6. Install dependencies and create the three demo users:

```powershell
cd backend
npm install
npm run seed
cd ..
cd ai-service
python -m pip install -r requirements.txt
cd ..
cd frontend
npm install
cd ..
```

## EVERY TIME YOU RUN IT

Run from project root:

```powershell
powershell -ExecutionPolicy Bypass -File .\START-WINDOWS.ps1
```

Or open three terminals manually:

```powershell
cd ai-service
python -m uvicorn main:app --reload --port 8000
```

```powershell
cd backend
npm start
```

```powershell
cd frontend
npm run dev
```

Open http://localhost:5173. Backend health: http://localhost:5000/api/health. AI docs: http://localhost:8000/docs.

## DEMO ACCOUNTS

All use the `DEMO_PASSWORD` you set in backend/.env (seeded with `npm run seed`).

- Admin: `admin@trustmark.local`
- Creator: `creator@trustmark.local`
- Manager: `manager@trustmark.local`

## Demo steps
1. Sign in as Admin → Guidelines → change rules → Save.
2. Logout → Creator → Analyze sample draft → accept/reject suggestions → Save draft → Submit for approval.
3. Logout → Manager → Approvals → Approve or Request changes.
4. Dashboard shows persistent counts; History shows who acted and when.
5. Restart backend; records persist in MongoDB.

## Known limitations and security
- Hackathon starter, **not production-hardened**. Demo accounts and a single shared brand, no multi-tenant isolation, no refresh-token flow, no virus scanning, no rate limiting, no structured audit immutability.
- Rule-based findings are heuristics. Gemini findings require verification; `sourceId` is validated against available guideline IDs but the evidence wording is not independently proven.
- PDF text extraction works for text PDFs; scanned images need OCR (not included).
- PDF/DOCX upload files are processed in memory and not retained. Do not upload sensitive documents to a public demo.
- The Gemini key stays server-side. Never commit `.env` files. Configure CORS and HTTPS for any public deployment.
- Dashboard metrics reflect submissions visible to the signed-in role (Creators see their own).
- Before deployment add tests, robust request validation, rate limits, secure cookies or carefully designed token storage, and a private deployment configuration.
