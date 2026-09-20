"""
IS-SARATHI Analyze API Endpoint
Implements domain detection, scope quality gate, evidence-grounded scoring, and abstention.
"""

import time
import uuid
import re
import logging
from typing import List, Dict, Any, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.standard import Standard, StandardClause, StandardRelationship
from app.models.decision import AuditLog
from app.schemas.analyze import (
    TenderAnalysisRequest,
    TenderAnalysisResponse,
    StandardRecommendation,
    ExtractedParameter,
    CoverageItem,
    ConflictItem,
    WhyNotItem,
    KeyClause,
    CertificationDetail,
    RelatedStandardDetail
)
from app.services.nlp_service import nlp_service
from app.services.embedding_service import embedding_service
from app.services.pinecone_service import pinecone_service
from app.services.local_ai_engine import local_ai_engine
from app.services.redis_service import redis_service
from app.services.scope_validator import scope_validator

logger = logging.getLogger("is_sarathi.api.analyze")
router = APIRouter(prefix="/analyze", tags=["Analyze"])


def _get_clauses_from_db(db: Session, standard_id: str) -> List[KeyClause]:
    """Queries child clauses belonging strictly to standard_id."""
    db_clauses = db.query(StandardClause).filter(
        StandardClause.standard_id == standard_id
    ).all()
    if db_clauses:
        return [KeyClause(clause=c.clause_number, title=c.title) for c in db_clauses]
    return []


def _get_verified_relationships_from_db(db: Session, standard_id: str) -> List[RelatedStandardDetail]:
    """Queries verified relationships from StandardRelationship table."""
    rels = db.query(StandardRelationship).filter(
        StandardRelationship.from_standard_id == standard_id
    ).all()

    result = []
    for r in rels:
        to_std = db.query(Standard).filter(Standard.id == r.to_standard_id).first()
        if to_std:
            result.append(RelatedStandardDetail(
                type=r.relationship_type or "Related Standard",
                isNumber=to_std.is_number,
                title=to_std.title,
                description=r.description or to_std.scope
            ))
    return result


def _is_subtype_compatible(primary_title: str, candidate_title: str) -> bool:
    """Verifies product sub-type compatibility to prevent cross-product secondary recommendations."""
    p_title = primary_title.lower()
    c_title = candidate_title.lower()

    # Product sub-type keyword clusters
    clusters = [
        ["cable", "wiring", "conductor", "wire"],
        ["pipe", "tubing", "tubular", "fitting", "conduit"],
        ["helmet", "headgear", "headform"],
        ["cement", "concrete", "rebar", "aggregate"],
        ["cylinder", "valve", "vessel"],
        ["water", "bottle", "packaging", "plastic"]
    ]

    for cluster in clusters:
        p_match = any(kw in p_title for kw in cluster)
        c_match = any(kw in c_title for kw in cluster)
        if p_match:
            return c_match

    return True


@router.post("", response_model=TenderAnalysisResponse)
def analyze_tender_specification(req: TenderAnalysisRequest, db: Session = Depends(get_db)):
    start_time = time.time()
    query_text = req.query.strip()
    if not query_text:
        raise HTTPException(status_code=400, detail="Tender specification text cannot be empty.")

    cache_key = f"analysis:{hash(query_text)}"
    cached_data = redis_service.get(cache_key)
    if cached_data:
        logger.info(f"Cache hit for query: '{query_text[:40]}...'")
        return cached_data

    # Stage 1: NLP Requirement Extraction
    extracted_raw = nlp_service.extract_requirements(query_text)
    extracted_params = [
        ExtractedParameter(
            field=p["field"],
            value=p["value"],
            category=p["category"],
            confidence=p["confidence"]
        ) for p in extracted_raw
    ]

    # Stage 2: Domain Detection
    detected_domain = scope_validator.detect_domain(query_text, extracted_raw)
    logger.info(f"Detected domain: '{detected_domain}' for query: '{query_text[:60]}'")

    # Stage 3: Vector Embeddings & Similarity Search
    query_vec = embedding_service.embed_text(query_text)
    vector_matches = pinecone_service.query_similarity(
        query_vector=query_vec,
        top_k=20,
        category_filter=req.category_filter
    )
    vector_score_map = {m["id"]: m["score"] for m in vector_matches}

    # Stage 4: Hybrid Scoring (no token splitting on "&")
    stop_words = {
        'the', 'a', 'an', 'for', 'with', 'and', 'in', 'of', 'to', 'at', 'on', 'by',
        'we', 'need', 'procurement', 'supply', 'require', 'procure', 'government',
        'project', 'specification', 'identify', 'applicable', 'related', 'testing',
        'standards', 'current', 'status', 'certification', 'requirements'
    }
    q_words = set(re.findall(r'[a-zA-Z0-9]+', query_text.lower())) - stop_words

    all_standards = db.query(Standard).all()
    scored_candidates = []

    for std in all_standards:
        title_words = set(re.findall(r'[a-zA-Z0-9]+', (std.title + " " + std.is_number).lower()))
        scope_words = set(re.findall(r'[a-zA-Z0-9]+', std.scope.lower()))

        title_hits = len(q_words & title_words)
        scope_hits = len(q_words & scope_words)

        lexical_score = (title_hits * 0.65 + scope_hits * 0.35) / max(len(q_words), 1)
        lexical_score = min(lexical_score, 1.0)
        semantic_score = vector_score_map.get(std.id, 0.0)

        cat_fit = 0.0
        if detected_domain and std.category:
            std_cat = std.category.strip()
            if std_cat == detected_domain:
                cat_fit = 1.0
            else:
                dom_words = set(re.findall(r'[a-zA-Z]{4,}', detected_domain.lower()))
                cat_words = set(re.findall(r'[a-zA-Z]{4,}', std_cat.lower()))
                shared = dom_words & cat_words
                if len(shared) >= 2:
                    cat_fit = 0.80

        hybrid_score = (0.50 * semantic_score) + (0.35 * lexical_score) + (0.15 * cat_fit)

        scored_candidates.append({
            "std": std,
            "hybrid_score": hybrid_score,
            "semantic_score": semantic_score,
            "lexical_score": lexical_score,
            "cat_fit": cat_fit
        })

    scored_candidates.sort(key=lambda x: x["hybrid_score"], reverse=True)

    # Stage 5: HARD SCOPE COMPATIBILITY FILTER
    compatible_candidates = []
    rejected_candidates = []

    for sc in scored_candidates[:20]:
        std = sc["std"]
        decision, scope_score, reason = scope_validator.evaluate_candidate_compatibility(
            query_text=query_text,
            domain=detected_domain,
            std_title=std.title,
            std_scope=std.scope,
            std_category=std.category or ""
        )
        sc["scope_decision"] = decision
        sc["scope_reason"] = reason
        sc["scope_score"] = scope_score

        if decision == "INCOMPATIBLE":
            rejected_candidates.append(sc)
            logger.info(f"REJECTED [{std.is_number}] — {reason}")
        else:
            compatible_candidates.append(sc)

    # Stage 6: Abstention Engine — 0 compatible standards or domain unrepresented in KB
    if not compatible_candidates:
        logger.warning(f"ABSTENTION: No compatible standards for: '{query_text[:80]}'")
        duration_ms = round((time.time() - start_time) * 1000, 2)
        audit_id = str(uuid.uuid4())
        try:
            log_entry = AuditLog(
                action="ANALYZE_TENDER_ABSTAIN",
                entity_type="TENDER_SPEC",
                entity_id=audit_id,
                details={
                    "query": query_text[:200],
                    "matched_standard": None,
                    "confidence": 0.0,
                    "duration_ms": duration_ms,
                    "reason": f"No verified domain-compatible standards found for '{detected_domain or 'Unknown'}'"
                }
            )
            db.add(log_entry)
            db.commit()
        except Exception as e:
            logger.warning(f"Could not write audit log: {e}")

        domain_msg = f"for domain '{detected_domain}'" if detected_domain else "in the current dataset"
        return TenderAnalysisResponse(
            tenderQuery=query_text,
            extractedRequirements=extracted_params,
            recommendations=[],
            conflicts=[],
            gaps=[
                "NO APPLICABLE STANDARD FOUND IN CURRENT DATASET",
                f"The requested procurement requirement is not covered by the current IS-SARATHI knowledge base ({domain_msg}).",
                "Official BIS catalog search / human verification recommended."
            ],
            processingTimeMs=duration_ms,
            abstentionReason=(
                "NO APPLICABLE STANDARD FOUND IN CURRENT DATASET — "
                "The requested procurement requirement is not covered by the current IS-SARATHI knowledge base."
            ),
            status="NOT_FOUND_IN_DATASET",
            auditTrailId=audit_id
        )

    # Build retrieved records from compatible candidates
    retrieved_records = []
    for sc in compatible_candidates[:8]:
        std = sc["std"]
        retrieved_records.append({
            "id": std.id,
            "is_number": std.is_number,
            "title": std.title,
            "scope": std.scope,
            "category": std.category,
            "status": std.status,
            "latest_version": std.latest_version or std.is_number,
            "amendment": std.amendment or "None",
            "certification_required": std.certification_required,
            "certification_scheme": std.certification_scheme or "BIS ISI Mark",
            "certification_status": std.certification_status or "Voluntary",
            "similarity_score": round(sc["hybrid_score"], 3),
            "scope_decision": sc.get("scope_decision", "COMPATIBLE"),
            "scope_reason": sc.get("scope_reason", ""),
            "clauses": std.clauses,
            "relationships": std.relationships_from
        })

    rejected_records = []
    for sc in rejected_candidates[:6]:
        std = sc["std"]
        rejected_records.append({
            "id": std.id,
            "is_number": std.is_number,
            "title": std.title,
            "scope": std.scope,
            "category": std.category,
            "similarity_score": round(sc["hybrid_score"], 3),
            "scope_decision": sc.get("scope_decision", "INCOMPATIBLE"),
            "scope_reason": sc.get("scope_reason", "Domain or product scope incompatibility.")
        })

    # Stage 7: AI Reasoning Engine
    ai_result = local_ai_engine.analyze_tender(
        query=query_text,
        extracted_params=extracted_raw,
        retrieved_standards=retrieved_records,
        detected_domain=detected_domain,
        rejected_standards=rejected_records
    )

    # Stage 8: Assemble Recommendations with strict clause integrity & verified relationships
    recommendations = []

    if retrieved_records:
        primary = retrieved_records[0]
        primary_id = primary["id"]

        # Strict clause referential integrity: clause.standard_id == standard.id
        key_clauses = _get_clauses_from_db(db, primary_id)
        # Verified relationships directly from database table
        related_stds = _get_verified_relationships_from_db(db, primary_id)

        conf = ai_result["confidence"]
        if conf >= 85:
            evidence_tier = "HIGH EVIDENCE"
        elif conf >= 70:
            evidence_tier = "MEDIUM EVIDENCE"
        else:
            evidence_tier = "LOW EVIDENCE — Verify"

        recommendations.append(StandardRecommendation(
            isNumber=primary["is_number"],
            title=primary["title"],
            type="Primary Standard",
            confidence=ai_result["confidence"],
            status=primary["status"],
            latestVersion=primary["latest_version"],
            amendment=primary["amendment"],
            certification=CertificationDetail(
                required=primary["certification_required"],
                scheme=primary["certification_scheme"],
                status=primary["certification_status"]
            ),
            category=primary["category"] or "General Standard",
            description=primary["scope"],
            keyClauses=key_clauses,
            relatedStandards=related_stds,
            coverageMap=[CoverageItem(**item) for item in ai_result["coverage_map"]],
            whyNotAlternatives=[WhyNotItem(**item) for item in ai_result["why_not_alternatives"]],
            evidenceTier=evidence_tier
        ))

        # Secondary recommendations: MUST match primary's product sub-type
        primary_title = primary.get("title", "")
        primary_cat = primary.get("category", "")

        for sec in retrieved_records[1:4]:
            sec_cat = sec.get("category", "")
            sec_sim = sec.get("similarity_score", 0.0)
            sec_title = sec.get("title", "")

            # Verify sub-type compatibility before adding as secondary recommendation
            if (
                sec_cat == primary_cat
                and sec_sim >= 0.20
                and sec["is_number"] != primary["is_number"]
                and _is_subtype_compatible(primary_title, sec_title)
            ):
                sec_clauses = _get_clauses_from_db(db, sec["id"])
                recommendations.append(StandardRecommendation(
                    isNumber=sec["is_number"],
                    title=sec["title"],
                    type="Related Standard",
                    confidence=round(ai_result["confidence"] * 0.82, 1),
                    status=sec["status"],
                    latestVersion=sec["latest_version"],
                    amendment=sec["amendment"],
                    certification=CertificationDetail(
                        required=sec["certification_required"],
                        scheme=sec["certification_scheme"],
                        status=sec["certification_status"]
                    ),
                    category=sec["category"] or "Allied Standard",
                    description=sec["scope"],
                    keyClauses=sec_clauses,
                    relatedStandards=[],
                    coverageMap=[],
                    whyNotAlternatives=[],
                    evidenceTier="MEDIUM EVIDENCE"
                ))

    duration_ms = round((time.time() - start_time) * 1000, 2)
    audit_id = str(uuid.uuid4())

    try:
        log_entry = AuditLog(
            action="ANALYZE_TENDER",
            entity_type="TENDER_SPEC",
            entity_id=audit_id,
            details={
                "query": query_text[:200],
                "detected_domain": detected_domain,
                "matched_standard": recommendations[0].isNumber if recommendations else None,
                "confidence": ai_result["confidence"],
                "compatible_count": len(compatible_candidates),
                "rejected_count": len(rejected_candidates),
                "duration_ms": duration_ms
            }
        )
        db.add(log_entry)
        db.commit()
    except Exception as e:
        logger.warning(f"Could not write audit log: {e}")

    response = TenderAnalysisResponse(
        tenderQuery=query_text,
        extractedRequirements=extracted_params,
        recommendations=recommendations,
        conflicts=[ConflictItem(**c) for c in ai_result["conflicts"]],
        gaps=ai_result["gaps"],
        processingTimeMs=duration_ms,
        abstentionReason=ai_result.get("abstention_reason"),
        status="MATCH_FOUND",
        auditTrailId=audit_id
    )

    redis_service.set(cache_key, response.model_dump(), ttl_seconds=1800)
    return response
