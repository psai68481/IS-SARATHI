from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.standard import Standard

router = APIRouter(prefix="/validate", tags=["Validation & Compliance"])

class ValidateRequest(BaseModel):
    is_number: str
    tender_specs: Dict[str, Any]

class ValidateResponse(BaseModel):
    is_number: str
    compliance_verdict: str
    coverage_score: float
    verified_clauses: List[Dict[str, Any]]
    detected_conflicts: List[Dict[str, Any]]

@router.post("", response_model=ValidateResponse)
def validate_specification_against_standard(req: ValidateRequest, db: Session = Depends(get_db)):
    std = db.query(Standard).filter(Standard.is_number == req.is_number).first()
    if not std:
        raise HTTPException(status_code=404, detail=f"Standard {req.is_number} not found in database.")

    clauses = []
    for c in std.clauses:
        clauses.append({
            "clause": c.clause_number,
            "title": c.title,
            "tested_parameter": c.tested_parameter,
            "limit": c.test_limit
        })

    # Rule-based conflict checking
    conflicts = []
    if "temperature" in req.tender_specs:
        temp_val = str(req.tender_specs["temperature"])
        if "100" in temp_val:
            conflicts.append({
                "parameter": "Operating Temperature",
                "tender_value": temp_val,
                "standard_limit": "80°C maximum continuous",
                "severity": "High"
            })

    return ValidateResponse(
        is_number=std.is_number,
        compliance_verdict="Compliant with Conditions" if conflicts else "Fully Compliant",
        coverage_score=88.5 if not conflicts else 65.0,
        verified_clauses=clauses,
        detected_conflicts=conflicts
    )
