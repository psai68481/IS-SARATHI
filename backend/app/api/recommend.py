from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.standard import Standard
from app.schemas.analyze import StandardRecommendation, CertificationDetail

router = APIRouter(prefix="/recommend", tags=["Recommendations"])

@router.get("/top")
def get_top_recommendations(category: Optional[str] = None, limit: int = 5, db: Session = Depends(get_db)):
    query = db.query(Standard)
    if category:
        query = query.filter(Standard.category == category)
    stds = query.limit(limit).all()
    
    recs = []
    for s in stds:
        recs.append({
            "isNumber": s.is_number,
            "title": s.title,
            "type": "Verified Standard",
            "category": s.category,
            "status": s.status,
            "latestVersion": s.latest_version or s.is_number,
            "certification": {
                "required": s.certification_required,
                "scheme": s.certification_scheme or "BIS ISI Mark",
                "status": s.certification_status or "Voluntary"
            },
            "scope": s.scope
        })
    return recs
