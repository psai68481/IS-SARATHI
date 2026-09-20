"""
IS-SARATHI Analyze API Endpoint
Implements the evidence-first recommendation pipeline with abstention,
coverage mapping, conflict detection, related-standard discovery, and audit trail.
"""

import time
import uuid
import logging
from typing import List, Dict, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.decision import AuditLog
from app.models.standard import Standard
from app.schemas.analyze import (
    TenderAnalysisRequest,
    TenderAnalysisResponse,
    StandardRecommendation,
    ExtractedParameter,
    ConflictItem,
    KeyClause,
    CertificationDetail,
    StabilityReport,
    RejectedCandidate,
    ProcurementModel,
)
from app.services.evidence_service import evidence_service
from app.services.nlp_service import nlp_service

logger = logging.getLogger("is_sarathi.api.analyze")
router = APIRouter(prefix="/analyze", tags=["Analyze"])


@router.post("", response_model=TenderAnalysisResponse)
def analyze_tender_specification(req: TenderAnalysisRequest, db: Session = Depends(get_db)):
    start_time = time.time()
    query_text = (req.query or "").strip()
    if not query_text:
        raise HTTPException(status_code=400, detail="Tender specification text cannot be empty.")

    # Stage 1: structured requirement extraction (NLP)
    extracted_raw = nlp_service.extract_requirements(query_text)
    extracted_params = [
        ExtractedParameter(
            field=item.get("field", "Product Type"),
            value=item.get("value", "General Procurement Item"),
            category=item.get("category", "Classification"),
            confidence=float(item.get("confidence", 0.0)),
        )
        for item in extracted_raw
    ]

    # Stage 2: evidence-first recommendation pipeline
    # Optional Recommendation Stability Check: re-runs the pipeline under
    # one-at-a-time requirement perturbations (feature #24).
    if req.include_stability:
        analysis = evidence_service.analyze_with_stability(db, query_text)
    else:
        analysis = evidence_service.analyze_requirement(db, query_text)
    duration_ms = round((time.time() - start_time) * 1000, 2)
    audit_id = analysis.get("audit_id") or str(uuid.uuid4())

    recommendations = []
    for item in analysis.get("recommendations", []):
        related_standards = [
            {
                "type": rel.get("type", "Related"),
                "isNumber": rel.get("isNumber", ""),
                "title": rel.get("title", ""),
                "description": rel.get("description", ""),
            }
            for rel in item.get("relatedStandards", [])
        ]
        recommendations.append(
            StandardRecommendation(
                isNumber=item["isNumber"],
                title=item["title"],
                type=item.get("type", "Primary Standard"),
                confidence=float(item["confidence"]),
                status=item["status"],
                latestVersion=item["latestVersion"],
                amendment=item["amendment"],
                certification=CertificationDetail(
                    required=bool(item.get("certification", {}).get("required", False)),
                    scheme=item.get("certification", {}).get("scheme", "BIS ISI Mark"),
                    status=item.get("certification", {}).get("status", "Unknown"),
                ),
                category=item["category"],
                description=item["description"],
                keyClauses=[KeyClause(**clause) for clause in item.get("keyClauses", [])],
                relatedStandards=related_standards,
                coverageMap=[CoverageItemShim(**entry) for entry in item.get("coverageMap", [])],
                whyNotAlternatives=[WhyNotItemShim(**entry) for entry in item.get("whyNotAlternatives", [])],
                evidenceTier=item.get("evidenceTier", "MEDIUM EVIDENCE"),
                whyRecommended=item.get("whyRecommended"),
                matchedRequirements=item.get("matchedRequirements"),
                totalRequirements=item.get("totalRequirements"),
            )
        )

    conflicts = [ConflictItem(**item) for item in analysis.get("conflicts", [])]

    try:
        db.add(
            AuditLog(
                action="ANALYZE_TENDER",
                entity_type="TENDER_SPEC",
                entity_id=audit_id,
                details={
                    "query": query_text[:200],
                    "status": analysis.get("status"),
                    "detected_product": analysis.get("detected_product"),
                    "language": analysis.get("language"),
                    "recommendation_count": len(recommendations),
                    "human_verification_required": analysis.get("human_verification_required", False),
                    "duration_ms": duration_ms,
                },
            )
        )
        db.commit()
    except Exception as exc:  # pragma: no cover - audit log should never block analysis
        logger.warning("Could not write audit log: %s", exc)

    return TenderAnalysisResponse(
        tenderQuery=query_text,
        extractedRequirements=extracted_params,
        recommendations=recommendations,
        conflicts=conflicts,
        gaps=analysis.get("gaps", []),
        processingTimeMs=duration_ms,
        abstentionReason=analysis.get("abstention_reason"),
        status=analysis.get("status", "MATCH_FOUND"),
        auditTrailId=audit_id,
        detectedProduct=analysis.get("detected_product"),
        language=analysis.get("language", "en"),
        humanVerificationRequired=bool(analysis.get("human_verification_required", False)),
        semanticScore=analysis.get("semantic_score"),
        stability=StabilityReport(**analysis["stability"]) if analysis.get("stability") else None,
        rejectedCandidates=[RejectedCandidate(**rc) for rc in analysis.get("rejected_candidates", [])],
        procurementModel=ProcurementModel(**analysis["procurement_model"]) if analysis.get("procurement_model") else None,
        missingSpecifications=analysis.get("missing_specifications", []),
    )


# Local shims: reuse existing schema models without renaming across the codebase
from app.schemas.analyze import CoverageItem as CoverageItemShim  # noqa: E402
from app.schemas.analyze import WhyNotItem as WhyNotItemShim  # noqa: E402
