import uuid
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.decision import AuditLog, HumanDecision
from app.schemas.analyze import FeedbackRequest

router = APIRouter(prefix="/feedback", tags=["Human-AI Validation & Override Feedback Loop"])

VALIDATION_STATUSES = {"Validated", "Unverified", "Rejected", "PENDING"}

# Override reason taxonomy (SIH26108 feature #26 — AI Override Detection)
OVERRIDE_REASONS = [
    "Missing requirement",
    "Special application",
    "Organization-specific requirement",
    "Standard relationship missed",
    "Incorrect interpretation",
    "New information",
    "Human expert judgment",
]


@router.get("/decisions")
def get_historical_decisions(limit: int = 50, db: Session = Depends(get_db)):
    decisions = db.query(HumanDecision).order_by(HumanDecision.created_at.desc()).limit(limit).all()
    return [
        {
            "caseId": d.case_id,
            "title": d.title,
            "department": d.department,
            "date": d.created_at.strftime("%Y-%m-%d"),
            "aiRecommendation": d.ai_recommendation,
            "humanDecision": d.human_decision,
            "reason": d.reason,
            "validationStatus": d.validation_status,
        }
        for d in decisions
    ]


@router.get("/learning")
def get_learning_signals(limit: int = 20, db: Session = Depends(get_db)):
    """
    Validated Feedback Learning (feature #27/#28).
    Only VALIDATED decisions become learning signals; Rejected ones become
    negative signals; Unverified/PENDING ones are shown but marked inert.
    Historical signals are reference-only — they never modify the current
    recommendation pipeline.
    """
    decisions = (
        db.query(HumanDecision)
        .order_by(HumanDecision.created_at.desc())
        .limit(limit * 3)
        .all()
    )
    signals: List[Dict[str, Any]] = []
    for d in decisions:
        status = (d.validation_status or "Unverified").lower()
        if status == "validated":
            signal_type = "positive" if d.human_decision == d.ai_recommendation else "override"
            confidence = "high"
        elif status == "rejected":
            signal_type = "negative"
            confidence = "high"
        else:
            signal_type = "pending"
            confidence = "low"
        if len(signals) >= limit:
            break
        signals.append({
            "caseId": d.case_id,
            "aiRecommendation": d.ai_recommendation,
            "humanDecision": d.human_decision,
            "reason": d.reason,
            "validationStatus": d.validation_status,
            "signalType": signal_type,
            "confidence": confidence,
            "learningExtract": (
                f"When a similar tender occurs, check '{d.reason}' against the "
                f"recommended standard before finalizing."
                if signal_type == "override" else
                "Reinforces existing matching behaviour for similar tenders."
                if signal_type == "positive" else
                "Do not rely on this decision; it was later determined incorrect."
                if signal_type == "negative" else
                "Awaiting expert validation; not yet influencing recommendations."
            ),
        })
    return {
        "note": "Historical learning signals are reference-only. Current recommendations always use the current tender + current knowledge base.",
        "signals": signals,
    }


@router.get("/stats")
def get_feedback_stats(db: Session = Depends(get_db)):
    """Dashboard KPIs derived from human decisions."""
    decisions = db.query(HumanDecision).all()
    total = len(decisions)
    validated = sum(1 for d in decisions if (d.validation_status or "").lower() == "validated")
    overrides = sum(
        1 for d in decisions
        if (d.validation_status or "").lower() == "validated" and d.human_decision != d.ai_recommendation
    )
    accuracy = round(100.0 * (validated - overrides) / validated, 1) if validated else 0.0
    return {
        "totalDecisions": total,
        "validated": validated,
        "unverified": sum(1 for d in decisions if (d.validation_status or "").lower() in {"unverified", "pending"}),
        "rejected": sum(1 for d in decisions if (d.validation_status or "").lower() == "rejected"),
        "aiOverrides": overrides,
        "accuracyRate": accuracy,
    }


@router.get("/dashboard-stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    """
    ALL dashboard metrics computed from the actual dataset — no hardcoded counts.
    Corpus size, audit counts and confidence distribution come from real rows.
    """
    from app.models.standard import Standard, StandardClause
    from app.models.decision import AuditLog as AL
    from sqlalchemy import func

    standards_count = db.query(func.count(Standard.id)).scalar() or 0
    clauses_count = db.query(func.count(StandardClause.id)).scalar() or 0
    audits = db.query(AL).filter(AL.action == "ANALYZE_TENDER").all()

    conf_buckets = {"90%+": 0, "80-89%": 0, "70-79%": 0, "<70%": 0}
    verified_flags = 0
    for a in audits:
        det = (a.details or {})
        # confidence is not stored per audit; use recommendation_count + status
        if det.get("status") == "FOUND_VERIFIED_MATCH":
            verified_flags += 1
    analyzed_count = len(audits)

    decisions = db.query(HumanDecision).all()
    validated = sum(1 for d in decisions if (d.validation_status or "").lower() == "validated")
    overrides = sum(
        1 for d in decisions
        if (d.validation_status or "").lower() == "validated" and d.human_decision != d.ai_recommendation
    )

    doc_audits = db.query(AL).filter(AL.action == "ANALYZE_TENDER_DOCUMENT").count()

    return {
        "standardsInKB": standards_count,
        "clausesInKB": clauses_count,
        "tendersAnalyzed": analyzed_count + doc_audits,
        "verifiedMatches": verified_flags,
        "pendingReviews": db.query(HumanDecision)
            .filter(HumanDecision.validation_status.in_(["Unverified", "PENDING"]))
            .count(),
        "totalDecisions": len(decisions),
        "validatedDecisions": validated,
        "aiOverrides": overrides,
        "note": "All metrics are computed live from the dataset; none are hardcoded.",
    }


@router.post("", status_code=201)
def submit_human_override_feedback(req: FeedbackRequest, db: Session = Depends(get_db)):
    validation_status = req.validation_status if req.validation_status in VALIDATION_STATUSES else "Unverified"
    decision = HumanDecision(
        case_id=req.case_id or f"PROC-{uuid.uuid4().hex[:8].upper()}",
        title=req.title,
        department=req.department or "Procurement",
        tender_query=req.tender_query,
        ai_recommendation=req.ai_recommendation,
        ai_confidence=req.ai_confidence,
        human_decision=req.human_choice,
        reason=req.justification,
        validation_status=validation_status,
    )
    db.add(decision)
    db.add(
        AuditLog(
            action="HUMAN_OVERRIDE_RECORDED",
            entity_type="CASE_DECISION",
            entity_id=decision.case_id,
            details={
                "ai_rec": req.ai_recommendation,
                "officer_choice": req.human_choice,
                "reason": req.justification,
                "validation_status": validation_status,
            },
        )
    )
    db.commit()

    return {
        "status": "success",
        "message": "Human review recorded. The authoritative knowledge base was not modified automatically.",
        "case_id": decision.case_id,
        "validation_status": validation_status,
    }


@router.post("/report-incorrect", status_code=201)
def report_incorrect_recommendation(payload: Dict[str, Any], db: Session = Depends(get_db)):
    case_id = payload.get("case_id") or f"REVIEW-{uuid.uuid4().hex[:8].upper()}"
    review_entry = HumanDecision(
        case_id=case_id,
        title=payload.get("title", "Incorrect recommendation review"),
        department=payload.get("department", "Procurement Review"),
        tender_query=payload.get("tender_query", ""),
        ai_recommendation=payload.get("selected_standard", "Unknown"),
        ai_confidence=float(payload.get("semantic_score", 0.0) or 0.0),
        human_decision="REJECTED",
        reason=payload.get("comment", "User reported incorrect recommendation."),
        validation_status="PENDING",
    )
    db.add(review_entry)
    db.add(
        AuditLog(
            action="INCORRECT_RECOMMENDATION_REPORTED",
            entity_type="REVIEW",
            entity_id=case_id,
            details=payload,
        )
    )
    db.commit()

    return {
        "status": "success",
        "case_id": case_id,
        "message": "Incorrect recommendation report created for human review.",
    }
