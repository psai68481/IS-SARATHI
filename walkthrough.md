# IS-SARATHI — Complete Real-Life Production Architecture

## Overview
**IS-SARATHI** is an AI-powered recommendation engine designed for the **Smart India Hackathon 2026 (Problem Statement 26108)**. It converts unstructured procurement specifications into an evidence-backed shortlist of applicable Indian Standards, traversing normative references, evaluating requirement coverage, detecting specification conflicts, and verifying mandatory Quality Control Orders (QCOs).

---

## 🛠️ Complete Tech Stack Implementation

### 1. 🖥️ Frontend — Web Application
- **Framework**: Next.js 14 (App Router) + React 18 + TypeScript + Tailwind CSS
- **Features**:
  - Full TypeScript type-safety models (`src/types/index.ts`)
  - Live API integration with FastAPI backend (`src/lib/api.ts`)
  - 9 integrated dashboard tabs:
    1. **Dashboard**: High-level KPIs, confidence distribution chart, active tender spotlight.
    2. **Tender Analysis**: Live tokenization and parameter extraction using spaCy NLP.
    3. **AI Recommendations**: Primary and allied standard recommendations with grounded evidence.
    4. **Related Standards**: Normative, test method, and safety standard relationship graph.
    5. **Requirement Coverage**: Clause-by-clause mapping of tender specifications to standard clauses.
    6. **Conflicts & Gaps**: Thermal/mechanical limit violation detection (e.g. 100°C tender vs 80°C standard).
    7. **Why Not?**: Transparent disqualification reasons for rejected alternative candidates.
    8. **Historical Decisions**: Auditable archive of past procurement determinations.
    9. **AI Override & Learning**: Human-in-the-loop validation and governance logging.
  - **Export Report**: Printable GeM-style procurement standard alignment certificate.

### 2. ⚙️ Backend — APIs & Services
- **Framework**: FastAPI (Python 3.11/3.14)
- **Database**: PostgreSQL (with automatic zero-dependency SQLite fallback)
- **Cache**: Redis (with automatic in-memory dictionary fallback)
- **Endpoints**:
  - `POST /api/v1/analyze`: Full 6-stage NLP, vector search, and grounded AI reasoning pipeline.
  - `GET /api/v1/standards`: CRUD operations and category-based filtering.
  - `GET /api/v1/standards/{id}`: Detailed standard record with clauses and relationships.
  - `POST /api/v1/validate`: Clause validation and conflict detection for specific parameters.
  - `GET /api/v1/version/{is_number}`: Authoritative version and amendment status lookup.
  - `GET /api/v1/certification/mandatory`: Mandatory Quality Control Order (QCO) standards.
  - `GET /api/v1/feedback/decisions`: Historical human officer determinations.
  - `POST /api/v1/feedback`: Human-in-the-loop override logging with audit trail.
  - `POST /api/v1/auth/login` & `/register`: JWT role-based authentication (`government_officer`, `technical_expert`, `administrator`).

### 3. 🧠 Native On-Device AI & NLP (Zero External Dependency)
- **Self-Contained Local Reasoning Engine (`LocalAIStandardsEngine`)**:
  - Generates evidence-grounded *"Why Recommended?"* citations directly from standard clauses.
  - Generates *"Why Not?"* disqualification rationale for rejected alternatives.
  - Calculates calibrated confidence using the formula:
    $$\text{Confidence} = \alpha \cdot \text{Semantic} + \beta \cdot \text{Lexical} + \gamma \cdot \text{Coverage} - \delta \cdot \text{StatusPenalty}$$
- **spaCy NLP Pipeline**: Entity extraction, classification, parameter isolation (temperature, pressure, voltage, impact).
- **Embeddings**: Sentence Transformers (`all-MiniLM-L6-v2`) with local normalized semantic cosine similarity.
- **Vector Search**: Pinecone-compatible vector store with high-performance local index fallback.

### 4. 🗄️ Storage
- **PostgreSQL / SQLite**: Structured source of truth for 62 curated standards across 6 domains:
  - *PPE & Occupational Safety* (IS 2925, IS 15298, IS 4770, IS 9562, IS 9473...)
  - *Pipes & Plumbing* (IS 4985, IS 12235, IS 1239, IS 3589, IS 14333...)
  - *Electrical & Wiring* (IS 694, IS 1554, IS 7098, IS 3043, IS 1180, IS 8828...)
  - *Civil & Construction* (IS 269, IS 456, IS 1786, IS 383...)
  - *LPG & Gas Cylinders* (IS 3196, IS 8867...)
  - *Food Packaging & Water* (IS 14543, IS 9845, IS 10146...)
- **AWS S3 / Local Document Storage**: Storage service supporting PDF specification files and amendment gazettes.

### 5. 🚀 DevOps & Containerization
- **Docker Compose (`docker-compose.yml`)**: Multi-container orchestration for `frontend`, `backend`, `postgres`, and `redis`.
- **CI/CD**:
  - `.github/workflows/ci.yml` (GitHub Actions workflow)
  - `.gitlab-ci.yml` (GitLab CI/CD multi-stage pipeline)

---

## 🔑 How to Obtain API Keys (If You Ever Choose to Connect Cloud Services)

Although the engine is **100% self-contained and runs offline without any external keys**, here are the exact steps if you wish to connect external cloud services in production:

### 1. Google Gemini API Key
- **What it's for**: Cloud LLM reasoning and multilingual translation.
- **How to get it**:
  1. Visit [Google AI Studio](https://aistudio.google.com/).
  2. Sign in with your Google account.
  3. Click **"Get API key"** in the left sidebar.
  4. Click **"Create API key in new project"**.
  5. Copy the key and set it in your `.env`:
     ```env
     GEMINI_API_KEY=AIzaSy...
     ```
  - *Cost*: Free tier provides 15 requests per minute (RPM) with 1 million tokens/minute.

### 2. Pinecone Vector Database
- **What it's for**: Cloud serverless vector indexing.
- **How to get it**:
  1. Visit [Pinecone Console](https://www.pinecone.io/) and create a free account.
  2. In the dashboard, click **"API Keys"**.
  3. Copy your API key and region (e.g. `us-east-1`).
  4. Add to `.env`:
     ```env
     PINECONE_API_KEY=pcsk_...
     PINECONE_ENVIRONMENT=us-east-1
     PINECONE_INDEX_NAME=is-sarathi-standards
     ```
  - *Cost*: Free Starter tier includes 1 serverless index with up to 100,000 vectors.

### 3. AWS S3 (Document Storage)
- **What it's for**: Uploading and hosting standards PDF documents.
- **How to get it**:
  1. Log in to the [AWS Management Console](https://aws.amazon.com/).
  2. Go to **S3** and click **"Create bucket"** (e.g., `is-sarathi-standards-docs`).
  3. Go to **IAM** -> **Users** -> **Create user** (e.g., `sarathi-s3-user`).
  4. Under Permissions, attach policy `AmazonS3FullAccess`.
  5. Go to the user's **Security credentials** tab and click **"Create access key"**.
  6. Add to `.env`:
     ```env
     AWS_ACCESS_KEY_ID=AKIA...
     AWS_SECRET_ACCESS_KEY=wJalrX...
     AWS_REGION=ap-south-1
     AWS_S3_BUCKET=is-sarathi-standards-docs
     USE_LOCAL_STORAGE=false
     ```

---

## 🏃 How to Run the Application

### Option A: Direct Local Execution (Fastest, zero setup)

1. **Start the FastAPI AI Backend**:
   ```bash
   cd backend
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```
   - Swagger Documentation: `http://localhost:8000/docs`
   - Health Check: `http://localhost:8000/health`

2. **Start the Frontend**:
   ```bash
   npm run dev
   ```
   - Portal: `http://localhost:5173` (or `http://localhost:3000` with `cd frontend && npm run dev`)

### Option B: Docker Containerization
```bash
docker-compose up --build
```
This boots all 4 services: Next.js Frontend (`:3000`), FastAPI Backend (`:8000`), PostgreSQL (`:5432`), and Redis (`:6379`).
