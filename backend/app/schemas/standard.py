from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class CertificationInfo(BaseModel):
    required: bool = False
    scheme: Optional[str] = "BIS ISI Mark"
    status: Optional[str] = "Voluntary"
    qco_notification_number: Optional[str] = None

class ClauseInfo(BaseModel):
    clause_number: str
    title: str
    requirement_text: Optional[str] = None
    tested_parameter: Optional[str] = None
    test_limit: Optional[str] = None

class RelatedStandardInfo(BaseModel):
    relationship_type: str # Test Method, Safety Standard, Material Standard, Normative Reference
    is_number: str
    title: str
    description: Optional[str] = None

class StandardBase(BaseModel):
    is_number: str = Field(..., example="IS 2925:1984")
    title: str = Field(..., example="Industrial Safety Helmets - Specification")
    scope: str
    ics_code: Optional[str] = "13.340.20"
    category: Optional[str] = "Personal Protective Equipment"
    status: Optional[str] = "CURRENT"
    revision_year: Optional[int] = 1984
    latest_version: Optional[str] = "IS 2925:1984 (Reaffirmed 2020)"
    amendment: Optional[str] = "Amendment 2, 2019"
    certification_required: bool = True
    certification_scheme: Optional[str] = "BIS ISI Mark"
    certification_status: Optional[str] = "Mandatory"
    qco_notification_number: Optional[str] = "S.O. 1234(E)"
    source_url: Optional[str] = "https://standards.bis.gov.in"

class StandardCreate(StandardBase):
    pass

class StandardUpdate(BaseModel):
    title: Optional[str] = None
    scope: Optional[str] = None
    ics_code: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None
    latest_version: Optional[str] = None
    amendment: Optional[str] = None
    certification_required: Optional[bool] = None
    certification_scheme: Optional[str] = None
    certification_status: Optional[str] = None

class StandardResponse(StandardBase):
    id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    related_standards: List[RelatedStandardInfo] = []
    clauses: List[ClauseInfo] = []

    class Config:
        from_attributes = True
