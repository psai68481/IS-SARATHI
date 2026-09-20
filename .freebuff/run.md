# IS-SARATHI — Run & Reproduce

## Reproduce the artifacts (fresh checkout)

1. **Frontend deps** (Next.js 15 + recharts + lucide-react):
   ```
   cd frontend && npm install
   ```
   `frontend/package-lock.json` is committed to this thread's workspace.
   No `.env.local` is required (API base URL defaults to `http://localhost:8000/api/v1`;
   override with `NEXT_PUBLIC_API_BASE_URL` if the backend runs elsewhere).

2. **Backend deps** (Python 3.12+):
   ```
   cd backend && pip install -r requirements.txt
   ```
   Core: fastapi, uvicorn, sqlalchemy, pydantic, pypdf (PDF text layer),
   pytesseract + pdf2image + Pillow (OCR for scanned PDFs / PNG / JPG — optional,
   degrades gracefully), numpy. spaCy `en_core_web_sm` is optional (regex engine
   is the fallback). Pinecone is optional (local in-memory vector index is the fallback).

3. **Database**: nothing to do — `backend/is_sarathi.db` is auto-created and
   auto-seeded (28 verified standards, 65 clause rows, relationships, users) on
   first backend startup. If the schema changed between runs, delete
   `is_sarathi.db` and restart (old snapshots are kept as `is_sarathi.db.old*`).

## Run the servers

- **Backend (FastAPI, port 8000)**:
  ```
  cd backend && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
  ```
  Health check: `GET http://127.0.0.1:8000/health` → 200.

- **Frontend (Next.js, port 3000)** — production mode after `npm run build`:
  ```
  cd frontend && npx next start -p 3000
  ```
  (or dev mode: `npm run dev`; when detaching on Windows use Start-Process with
  stdout and stderr redirected to DIFFERENT files).
  Confirm the pid survives (`Get-Process -Id <pid>`) and `http://localhost:3000/` answers 200.

- **Single-origin API**: the frontend calls `/api/v1/*` (relative); Next.js rewrites
  proxy it to `http://localhost:8000/api/v1/*` (see `frontend/next.config.js`).
  Verify with: `curl http://localhost:3000/api/v1/feedback/dashboard-stats` → 200.

- **Production deployment (PERMANENT — Vercel)**: https://is-sarathi.vercel.app
  - Architecture: Vercel Services multi-service project `is-sarathi`
    (account `pabbasaipavan123-5403s-projects`):
    - `web`  → `frontend/` (Next.js, framework-detected)
    - `api`  → `backend/` (Docker container from `backend/Dockerfile.vercel`:
      python:3.12-slim + tesseract-ocr [eng/hin/tel] + poppler-utils; uvicorn on $PORT)
    - Routing (`vercel.json` rewrites): `/api/v1/*`, `/health`, `/docs`, `/openapi.json`
      → api service; everything else → web service. One public origin, no CORS needed.
  - Database: Vercel Marketplace **Neon Postgres** (free tier), resource env vars
    (`DATABASE_URL` et al.) attached automatically to the project. Schema is created
    and seeded on first boot (`app.main` lifespan → `Base.metadata.create_all` +
    `seed_database_and_vectors`).
  - Secrets (Vercel env, Production scope): `JWT_SECRET_KEY` (random 48-byte token),
    `ENVIRONMENT=production`, `REDIS_ENABLED=false`. Vector DB: add `PINECONE_API_KEY`
    the same way to activate the Pinecone serverless index (local in-memory vector
    index is the automatic fallback).
  - Redeploy after changes: `npx vercel deploy --prod --yes` from the repo root.
  - Uploads: Vercel Functions cap request bodies at 4.5 MB — the upload UI guards
    this client-side; the backend's own 20 MB guard remains for non-Vercel hosts.
  - Optional auto-deploy on git push: connect GitHub at
    Dashboard → is-sarathi → Settings → Git Connection (requires a one-time
    GitHub Login Connection on the Vercel account).

- Preview log file: `.freebuff/preview-<threadid>.log` (+ `.log.err` for stderr).

## Verify the generic engine (quick smoke)

- `POST /api/v1/analyze {"query":"industrial safety helmets for construction workers with impact resistance and electrical insulation"}` → `FOUND_VERIFIED_MATCH`, top `IS 2925:1984`, glove standard appears in `rejectedCandidates` with `REJECTED_PRODUCT_MISMATCH`.
- `POST /api/v1/analyze {"query":"5000 metres structural steel"}` → abstains (`LOW_CONFIDENCE`); steel-form standards rejected by `REJECTED_MATERIAL_MISMATCH` (material-only matching can never recommend).
- `POST /api/v1/analyze {"query":"fire extinguishers"}` → `NOT_FOUND_IN_DATASET` (dataset boundary).
- `POST /api/v1/analyze {"query":"100°C helmets"}` → `FOUND_PARTIAL_MATCH` with a conflict flag (tender 100°C vs clause rating 50°C).
- `POST /api/v1/feedback/dashboard-stats` → all metrics computed live (no hardcoded counts).
- `POST /api/v1/analyze-document` (multipart PDF/PNG/JPG/TXT) → same pipeline + provenance; scanned uploads get OCR or a `LOW_OCR_CONFIDENCE` flag.

Backend tests: `cd backend && python -m pytest tests/ -q` (38 tests: positive matrix, adversarial, multilingual, dataset-boundary, clause-provenance).
Frontend: `cd frontend && npx tsc --noEmit && npm run build`.
