import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base, SessionLocal
from app.seed.standards_seed import seed_database_and_vectors

# Import API routers
from app.api.auth import router as auth_router
from app.api.standards import router as standards_router
from app.api.analyze import router as analyze_router
from app.api.analyze_document import router as analyze_document_router
from app.api.recommend import router as recommend_router
from app.api.validate import router as validate_router
from app.api.version import router as version_router
from app.api.certification import router as certification_router
from app.api.feedback import router as feedback_router

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("is_sarathi.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing IS-SARATHI Database & Tables...")
    Base.metadata.create_all(bind=engine)

    # Auto-seed database and vector index
    try:
        db = SessionLocal()
        seed_database_and_vectors(db)
        db.close()
    except Exception as e:
        logger.warning(f"Database seed notice: {e}")

    logger.info("IS-SARATHI AI Recommendation Engine Ready on " + settings.API_V1_PREFIX)
    yield
    logger.info("Shutting down IS-SARATHI Engine...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="AI-Powered Recommendation Engine for Identifying Applicable Indian Standards for Procurement Specifications (Smart India Hackathon 2026 PS 26108)",
    lifespan=lifespan
)

# Setup CORS: locked down in production via ALLOWED_ORIGINS env var;
# wildcard only when no explicit production origin is configured.
_origins = settings.cors_origins
if settings.ENVIRONMENT != "production":
    _origins = list(set(_origins + ["http://localhost:3000", "http://127.0.0.1:3000"]))

app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Endpoints
prefix = settings.API_V1_PREFIX
app.include_router(auth_router, prefix=prefix)
app.include_router(standards_router, prefix=prefix)
app.include_router(analyze_router, prefix=prefix)
app.include_router(analyze_document_router, prefix=prefix)
app.include_router(recommend_router, prefix=prefix)
app.include_router(validate_router, prefix=prefix)
app.include_router(certification_router, prefix=prefix)
app.include_router(feedback_router, prefix=prefix)

@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": "IS-SARATHI AI Backend",
        "ai_engine": "Native On-Device (Zero External Dependency)",
        "nlp": "spaCy + Sentence Transformers",
        "version": "1.0.0"
    }

@app.get("/", tags=["Root"])
def root():
    return {
        "project": "IS-SARATHI",
        "tagline": "AI-Powered Indian Standards Recommendation Engine for Procurement Specifications",
        "docs_url": "/docs",
        "health_url": "/health"
    }
