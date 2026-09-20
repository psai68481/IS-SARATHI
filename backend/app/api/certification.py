from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.standard import Standard

router = APIRouter(prefix="/certification", tags=["Certification Applicability & QCO"])

@router.get("/mandatory")
def list_mandatory_qco_standards(db: Session = Depends(get_db)):
    stds = db.query(Standard).filter(Standard.certification_status == "Mandatory").all()
    return [
        {
            "is_number": s.is_number,
            "title": s.title,
            "category": s.category,
            "certification_scheme": s.certification_scheme,
            "certification_status": s.certification_status,
            "qco_notification": s.qco_notification_number or "Ministry Quality Control Order"
        }
        for s in stds
    ]

@router.get("/{is_number:path}")
def check_certification(is_number: str, db: Session = Depends(get_db)):
    std = db.query(Standard).filter(Standard.is_number.ilike(f"%{is_number}%")).first()
    if not std:
        raise HTTPException(status_code=404, detail=f"Standard {is_number} not found.")

    return {
        "is_number": std.is_number,
        "title": std.title,
        "certification_required": std.certification_required,
        "certification_scheme": std.certification_scheme or "BIS ISI Mark",
        "certification_status": std.certification_status or "Voluntary",
        "qco_order": std.qco_notification_number or "Not under mandatory QCO",
        "legal_implication": "Mandatory BIS ISI Mark certification required prior to public procurement tender award." if std.certification_status == "Mandatory" else "Voluntary standard conformity."
    }
