"""
IS-SARATHI Document Upload API
==============================
Implements SIH26108 stages 1+4: tender document upload (PDF/TXT) ->
text extraction (with OCR fallback) -> requirement extraction -> the SAME
evidence-first recommendation pipeline used for pasted text.

POST /api/v1/analyze-document   (multipart/form-data)
    file              : the tender PDF/TXT
    include_stability : optional flag forwarded to the analyze pipeline
    prefer_ocr        : optional flag to force OCR even when a text layer exists

No separate recommendation path is introduced - extracted text flows into
evidence_service.analyze_requirement exactly like a pasted tender.
"""

import logging
import time
import uuid

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from typing import Dict, Any
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.decision import AuditLog
from app.schemas.analyze import (
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
from app.services.document_service import document_service, SUPPORTED_EXTENSIONS
from app.services.evidence_service import evidence_service
from app.services.nlp_service import nlp_service

logger = logging.getLogger("is_sarathi.api.analyze_document")
router = APIRouter(prefix="/analyze-document", tags=["Tender Document Upload"])


def _truthy(form_value) -> bool:
    return str(form_value or "").strip().lower() in {"1", "true", "yes", "on"}


@router.post("", response_model=TenderAnalysisResponse)
async def analyze_tender_document(
    file: UploadFile = File(..., description="Tender document (PDF or TXT)"),
    include_stability: str = Form("false"),
    prefer_ocr: str = Form("false"),
    department: str = Form("Public Works Department (PWD)"),
    db: Session = Depends(get_db),
):
    start_time = time.time()

    # ------------------------------------------------------------------
    # 1. Read + validate upload
    # ------------------------------------------------------------------
    filename = file.filename or "tender.pdf"
    lower = filename.lower()
    if not any(lower.endswith(ext) for ext in SUPPORTED_EXTENSIONS):
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Upload a PDF, TXT, PNG or JPG tender document.",
        )

    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    # ------------------------------------------------------------------
    # 2. Extract text (PDF text layer / OCR fallback / txt passthrough)
    # ------------------------------------------------------------------
    try:
        extraction = document_service.extract(
            filename, data, prefer_ocr=_truthy(prefer_ocr)
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))

    extracted_text = (extraction.get("text") or "").strip()
    warnings = list(extraction.get("warnings") or [])

    if not extracted_text:
        raise HTTPException(
            status_code=422,
            detail=(
                "No machine-readable text could be extracted from this document. "
                + " ".join(warnings)
            ).strip(),
        )

    # ------------------------------------------------------------------
    # 3. Run the SAME evidence pipeline used for pasted tenders
    # ------------------------------------------------------------------
    if _truthy(include_stability):
        analysis = evidence_service.analyze_with_stability(db, extracted_text)
    else:
        analysis = evidence_service.analyze_requirement(db, extracted_text)

    duration_ms = round((time.time() - start_time) * 1000, 2)
    audit_id = analysis.get("audit_id") or str(uuid.uuid4())

    # Requirement extraction from the document text
    extracted_params = [
        ExtractedParameter(
            field=item.get("field", "Product Type"),
            value=item.get("value", "General Procurement Item"),
            category=item.get("category", "Classification"),
            confidence=float(item.get("confidence", 0.0)),
        )
        for item in nlp_service.extract_requirements(extracted_text)
    ]

    recommendations = []
    for item in analysis.get("recommendations", []):
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
                relatedStandards=[
                    {
                        "type": rel.get("type", "Related"),
                        "isNumber": rel.get("isNumber", ""),
                        "title": rel.get("title", ""),
                        "description": rel.get("description", ""),
                    }
                    for rel in item.get("relatedStandards", [])
                ],
                coverageMap=[CoverageItemShim(**entry) for entry in item.get("coverageMap", [])],
                whyNotAlternatives=[WhyNotItemShim(**entry) for entry in item.get("whyNotAlternatives", [])],
                evidenceTier=item.get("evidenceTier", "MEDIUM EVIDENCE"),
                whyRecommended=item.get("whyRecommended"),
                matchedRequirements=item.get("matchedRequirements"),
                totalRequirements=item.get("totalRequirements"),
            )
        )

    conflicts = [ConflictItem(**item) for item in analysis.get("conflicts", [])]

    # Document-processing warnings join the gap list so officers see them
    gaps = list(analysis.get("gaps") or []) + [
        f"Document note: {w}" for w in warnings
    ]

    # OCR uncertainty is surfaced explicitly — never guessed through.
    if extraction.get("low_ocr_confidence"):
        gaps.insert(0,
            "LOW_OCR_CONFIDENCE: extracted text is unreliable. Human verification "
            "of every extracted value is required before using this analysis."
        )

    # Provenance: where every analyzed word came from
    provenance = {
        "documentName": extraction.get("filename"),
        "pages": extraction.get("pages"),
        "extractionMethod": extraction.get("method"),
        "extractedChars": len(extracted_text),
        "language": extraction.get("language", "en"),
        "lowOcrConfidence": bool(extraction.get("low_ocr_confidence")),
        "note": "OCR extracts USER DOCUMENT information; it is NOT authoritative BIS evidence.",
    }

    # ------------------------------------------------------------------
    # 4. Audit trail
    # ------------------------------------------------------------------
    try:
        db.add(
            AuditLog(
                action="ANALYZE_TENDER_DOCUMENT",
                entity_type="TENDER_DOCUMENT",
                entity_id=audit_id,
                details={
                    "filename": extraction.get("filename"),
                    "size_bytes": extraction.get("size_bytes"),
                    "pages": extraction.get("pages"),
                    "extraction_method": extraction.get("method"),
                    "needs_ocr": extraction.get("needs_ocr", False),
                    "low_ocr_confidence": extraction.get("low_ocr_confidence", False),
                    "extracted_chars": len(extracted_text),
                    "status": analysis.get("status"),
                    "recommendation_count": len(recommendations),
                    "duration_ms": duration_ms,
                },
            )
        )
        db.commit()
    except Exception as exc:  # pragma: no cover - audit must never block analysis
        logger.warning("Could not write document audit log: %s", exc)

    return TenderAnalysisResponse(
        tenderQuery=extracted_text[:4000],
        extractedRequirements=extracted_params,
        recommendations=recommendations,
        conflicts=conflicts,
        gaps=gaps,
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
        documentProvenance=provenance,
    )


# Local shims (same pattern as analyze.py)
from app.schemas.analyze import CoverageItem as CoverageItemShim  # noqa: E402
from app.schemas.analyze import WhyNotItem as WhyNotItemShim  # noqa: E402
