from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.standard import Standard, StandardRelationship, StandardClause
from app.schemas.standard import StandardResponse, StandardCreate, StandardUpdate, RelatedStandardInfo, ClauseInfo

router = APIRouter(prefix="/standards", tags=["Standards Knowledge Base"])

@router.get("", response_model=List[StandardResponse])
def get_standards(
    skip: int = 0,
    limit: int = 50,
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Standard)
    if category:
        query = query.filter(Standard.category == category)
    if search:
        search_fmt = f"%{search}%"
        query = query.filter(
            (Standard.is_number.ilike(search_fmt)) |
            (Standard.title.ilike(search_fmt)) |
            (Standard.scope.ilike(search_fmt))
        )
    standards = query.offset(skip).limit(limit).all()
    
    results = []
    for s in standards:
        clauses = [
            ClauseInfo(
                clause_number=c.clause_number,
                title=c.title,
                requirement_text=c.requirement_text,
                tested_parameter=c.tested_parameter,
                test_limit=c.test_limit
            ) for c in s.clauses
        ]
        
        # Assemble relationships
        rels = []
        for r in s.relationships_from:
            target = r.to_standard
            if target:
                rels.append(RelatedStandardInfo(
                    relationship_type=r.relationship_type,
                    is_number=target.is_number,
                    title=target.title,
                    description=r.description
                ))

        results.append(StandardResponse(
            id=s.id,
            is_number=s.is_number,
            title=s.title,
            scope=s.scope,
            ics_code=s.ics_code,
            category=s.category,
            status=s.status,
            revision_year=s.revision_year,
            latest_version=s.latest_version,
            amendment=s.amendment,
            certification_required=s.certification_required,
            certification_scheme=s.certification_scheme,
            certification_status=s.certification_status,
            qco_notification_number=s.qco_notification_number,
            source_url=s.source_url,
            created_at=s.created_at,
            updated_at=s.updated_at,
            related_standards=rels,
            clauses=clauses
        ))
    return results

@router.get("/{standard_id}", response_model=StandardResponse)
def get_standard_by_id(standard_id: str, db: Session = Depends(get_db)):
    s = db.query(Standard).filter(Standard.id == standard_id).first()
    if not s:
        s = db.query(Standard).filter(Standard.is_number == standard_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Standard not found")

    clauses = [
        ClauseInfo(
            clause_number=c.clause_number,
            title=c.title,
            requirement_text=c.requirement_text,
            tested_parameter=c.tested_parameter,
            test_limit=c.test_limit
        ) for c in s.clauses
    ]
    
    rels = []
    for r in s.relationships_from:
        target = r.to_standard
        if target:
            rels.append(RelatedStandardInfo(
                relationship_type=r.relationship_type,
                is_number=target.is_number,
                title=target.title,
                description=r.description
            ))

    return StandardResponse(
        id=s.id,
        is_number=s.is_number,
        title=s.title,
        scope=s.scope,
        ics_code=s.ics_code,
        category=s.category,
        status=s.status,
        revision_year=s.revision_year,
        latest_version=s.latest_version,
        amendment=s.amendment,
        certification_required=s.certification_required,
        certification_scheme=s.certification_scheme,
        certification_status=s.certification_status,
        qco_notification_number=s.qco_notification_number,
        source_url=s.source_url,
        created_at=s.created_at,
        updated_at=s.updated_at,
        related_standards=rels,
        clauses=clauses
    )
