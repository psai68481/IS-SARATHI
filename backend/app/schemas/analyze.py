from typing import List, Optional, Any
from pydantic import BaseModel, Field

class StabilityVariant(BaseModel):
    kind: str                      # remove | emphasize
    requirement: str
    fragment: str
    perturbedQuery: str
    topStandard: Optional[str] = None
    topConfidence: float
    confidenceDelta: float
    flipped: bool
    abstained: bool
    sensitivity: float
    critical: bool
    verdict: str

class StabilitySummaryItem(BaseModel):
    requirement: str
    fragment: str
    maxDrop: float
    flippedOnRemove: bool
    abstainedOnRemove: bool
    emphasizeGain: float
    critical: bool

class StabilityReport(BaseModel):
    baselineTop: Optional[str] = None
    baselineConfidence: float
    overall: str                    # STABLE | MODERATE | FRAGILE | NOT_APPLICABLE
    checkedRequirements: int
    summary: List[StabilitySummaryItem] = []
    variants: List[StabilityVariant] = []
    note: str

class TenderAnalysisRequest(BaseModel):
    query: str = Field(..., example="We need industrial helmets for construction workers with impact resistance and electrical insulation")
    department: Optional[str] = "Public Works Department (PWD)"
    ics_filter: Optional[str] = None
    category_filter: Optional[str] = None
    include_stability: bool = Field(default=False, description="Run the Recommendation Stability Check (one-at-a-time perturbation re-analysis)")


class RejectedCandidate(BaseModel):
    """A retrieved standard rejected by the generic compatibility gates."""
    isNumber: str
    title: str
    similarityScore: float
    status: str
    reasons: List[str] = []
    failedChecks: List[str] = []


class ProcurementModel(BaseModel):
    """Structured procurement understanding surfaced for transparency/provenance."""
    product: str = ""
    productSubtype: List[str] = []
    materials: List[str] = []
    productForms: List[str] = []
    applications: List[str] = []
    quantity: Optional[str] = None
    unit: Optional[str] = None
    parameters: List[dict] = []
    isReferences: List[str] = []
    language: str = "en"

class ExtractedParameter(BaseModel):
    field: str
    value: str
    category: str
    confidence: float

class CoverageItem(BaseModel):
    requirement: str
    evidence: Optional[str] = None
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
    whyRecommended: Optional[str] = None
    matchedRequirements: Optional[int] = None
    totalRequirements: Optional[int] = None

class TenderAnalysisResponse(BaseModel):
    tenderQuery: str
    extractedRequirements: List[ExtractedParameter]
    recommendations: List[StandardRecommendation]
    conflicts: List[ConflictItem]
    gaps: List[str]
    processingTimeMs: float
    abstentionReason: Optional[str] = None
    status: Optional[str] = "MATCH_FOUND"  # FOUND_VERIFIED_MATCH | FOUND_PARTIAL_MATCH | LOW_CONFIDENCE | NOT_FOUND_IN_DATASET | REJECTED_SCOPE_INCOMPATIBLE | REQUIRES_HUMAN_VERIFICATION
    auditTrailId: str
    detectedProduct: Optional[str] = None
    language: Optional[str] = "en"
    humanVerificationRequired: bool = False
    semanticScore: Optional[float] = None
    stability: Optional[StabilityReport] = None
    rejectedCandidates: List[RejectedCandidate] = []
    procurementModel: Optional[ProcurementModel] = None
    missingSpecifications: List[str] = []
    documentProvenance: Optional[dict] = None  # provenance for uploaded-document analyses (name, pages, method, OCR confidence)

class FeedbackRequest(BaseModel):
    case_id: Optional[str] = None
    title: str
    department: Optional[str] = ""
    tender_query: str
    ai_recommendation: str
    ai_confidence: float
    human_choice: str
    justification: str
    validation_status: str = "Unverified"
