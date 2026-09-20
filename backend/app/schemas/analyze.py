from typing import List, Optional, Any
from pydantic import BaseModel, Field

class TenderAnalysisRequest(BaseModel):
    query: str = Field(..., example="We need industrial helmets for construction workers with impact resistance and electrical insulation")
    department: Optional[str] = "Public Works Department (PWD)"
    ics_filter: Optional[str] = None
    category_filter: Optional[str] = None

class ExtractedParameter(BaseModel):
    field: str
    value: str
    category: str
    confidence: float

class CoverageItem(BaseModel):
    requirement: str
    evidence: Optional[str]
    detail: str
    covered: bool

class ConflictItem(BaseModel):
    tenderSpec: str
    standardSpec: str
    severity: str # Warning, Critical, Notice
    impact: str

class WhyNotItem(BaseModel):
    isNumber: str
    title: str
    confidence: float
    reason: str

class KeyClause(BaseModel):
    clause: str
    title: str

class CertificationDetail(BaseModel):
    required: bool
    scheme: str
    status: str

class RelatedStandardDetail(BaseModel):
    type: str
    isNumber: str
    title: str
    description: str

class StandardRecommendation(BaseModel):
    isNumber: str
    title: str
    type: str # Primary Standard, Related Standard, Specialized Alternative
    confidence: float
    status: str
    latestVersion: str
    amendment: str
    certification: CertificationDetail
    category: str
    description: str
    keyClauses: List[KeyClause] = []
    relatedStandards: List[RelatedStandardDetail] = []
    coverageMap: List[CoverageItem] = []
    whyNotAlternatives: List[WhyNotItem] = []
    evidenceTier: Optional[str] = "MEDIUM EVIDENCE"

class TenderAnalysisResponse(BaseModel):
    tenderQuery: str
    extractedRequirements: List[ExtractedParameter]
    recommendations: List[StandardRecommendation]
    conflicts: List[ConflictItem]
    gaps: List[str]
    processingTimeMs: float
    abstentionReason: Optional[str] = None
    status: Optional[str] = "MATCH_FOUND"
    auditTrailId: str

class FeedbackRequest(BaseModel):
    case_id: str
    title: str
    department: str
    tender_query: str
    ai_recommendation: str
    ai_confidence: float
    human_choice: str
    justification: str
    validation_status: str = "Validated"
