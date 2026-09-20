from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.standard import Standard

router = APIRouter(prefix="/version", tags=["Version & Amendments"])

@router.get("/{is_number:path}")
def check_standard_version(is_number: str, db: Session = Depends(get_db)):
    std = db.query(Standard).filter(Standard.is_number.ilike(f"%{is_number}%")).first()
    if not std:
        raise HTTPException(status_code=404, detail=f"Standard {is_number} not found.")

    return {
        "is_number": std.is_number,
        "title": std.title,
        "status": std.status,
        "revision_year": std.revision_year,
        "latest_version": std.latest_version,
        "amendment": std.amendment or "No pending amendments",
        "verified_at": std.verified_at,
        "source": "Bureau of Indian Standards Official Gazette & Portal"
    }
