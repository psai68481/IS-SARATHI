// TypeScript Data Models for IS-SARATHI

export interface ExtractedRequirement {
  field: string;
  value: string;
  category: string;
  confidence: number;
}

export interface KeyClause {
  clause: string;
  title: string;
}

export interface RelatedStandard {
  type: string;
  isNumber: string;
  title: string;
  description: string;
}

export interface CoverageItem {
  requirement: string;
  evidence: string | null;
  detail: string;
  covered: boolean;
}

export interface WhyNotAlternative {
  isNumber: string;
  title: string;
  confidence: number;
  reason: string;
}

export interface CertificationInfo {
  required: boolean;
  scheme: string;
  status: string;
}

export interface StandardRecommendation {
  isNumber: string;
  title: string;
  type: string;
  confidence: number;
  status: string;
  latestVersion: string;
  amendment: string;
  certification: CertificationInfo;
  category: string;
  description: string;
  keyClauses: KeyClause[];
  relatedStandards: RelatedStandard[];
  coverageMap: CoverageItem[];
  whyNotAlternatives: WhyNotAlternative[];
  evidenceTier?: string;
  whyRecommended?: string;
  matchedRequirements?: number;
  totalRequirements?: number;
}

export interface RejectedCandidate {
  isNumber: string;
  title: string;
  similarityScore: number;
  status: string; // REJECTED_PRODUCT_MISMATCH | REJECTED_EXCLUDED | REJECTED_MATERIAL_MISMATCH | ...
  reasons: string[];
  failedChecks: string[];
}

export interface ProcurementModel {
  product: string;
  productSubtype: string[];
  materials: string[];
  productForms: string[];
  applications: string[];
  quantity: string | null;
  unit: string | null;
  parameters: { type: string; display: string }[];
  isReferences: string[];
  language: string;
}

export interface DocumentProvenance {
  documentName?: string | null;
  pages?: number | null;
  extractionMethod?: string | null;
  extractedChars?: number | null;
  language?: string | null;
  lowOcrConfidence?: boolean;
  note?: string | null;
}

export interface AnalyzeResponse {
  tenderQuery: string;
  extractedRequirements: ExtractedRequirement[];
  recommendations: StandardRecommendation[];
  conflicts: ConflictItem[];
  gaps: string[];
  processingTimeMs: number;
  abstentionReason?: string | null;
  status?: string;
  auditTrailId: string;
  detectedProduct?: string | null;
  language?: string;
  humanVerificationRequired?: boolean;
  semanticScore?: number;
  stability?: StabilityReport | null;
  rejectedCandidates?: RejectedCandidate[];
  procurementModel?: ProcurementModel | null;
  missingSpecifications?: string[];
  documentProvenance?: DocumentProvenance | null;
}

// Recommendation Stability Check (feature #24)
export interface StabilityVariant {
  kind: "remove" | "emphasize";
  requirement: string;
  fragment: string;
  perturbedQuery: string;
  topStandard: string | null;
  topConfidence: number;
  confidenceDelta: number;
  flipped: boolean;
  abstained: boolean;
  sensitivity: number;
  critical: boolean;
  verdict: string;
}

export interface StabilitySummaryItem {
  requirement: string;
  fragment: string;
  maxDrop: number;
  flippedOnRemove: boolean;
  abstainedOnRemove: boolean;
  emphasizeGain: number;
  critical: boolean;
}

export interface StabilityReport {
  baselineTop: string | null;
  baselineConfidence: number;
  overall: "STABLE" | "MODERATE" | "FRAGILE" | "NOT_APPLICABLE" | string;
  checkedRequirements: number;
  summary: StabilitySummaryItem[];
  variants: StabilityVariant[];
  note: string;
}

export interface HistoricalDecision {
  caseId: string;
  title: string;
  department: string;
  date: string;
  aiRecommendation: string;
  humanDecision: string;
  reason: string;
  validationStatus: "Validated" | "Unverified" | "Rejected";
}

export interface ConflictItem {
  tenderSpec: string;
  standardSpec: string;
  severity: string;
  impact: string;
}

export interface TenderPreset {
  id: string;
  title: string;
  query: string;
  department: string;
}

export interface SystemStats {
  totalTendersAnalyzed: number;
  avgConfidence: number;
  standardsInKB: number;
  pendingReviews: number;
  accuracyRate: number;
  avgProcessingTime: string;
  // dynamic backend metrics (dashboard-stats endpoint) — no fake numbers
  clausesInKB?: number;
  tendersAnalyzed?: number;
  verifiedMatches?: number;
  totalDecisions?: number;
  validatedDecisions?: number;
  aiOverrides?: number;
}

export interface ConfidenceDistItem {
  range: string;
  count: number;
  fill: string;
}

export interface DomainBreakdownItem {
  domain: string;
  count: number;
  share: string;
}

export interface DashboardData {
  tenderQuery: string;
  extractedRequirements: ExtractedRequirement[];
  recommendations: StandardRecommendation[];
  historicalDecisions: HistoricalDecision[];
  gaps: string[];
  conflicts: ConflictItem[];
  stats: SystemStats;
  confidenceDistribution: ConfidenceDistItem[];
  domainBreakdown: DomainBreakdownItem[];
  tenderPresets: TenderPreset[];
  stability?: StabilityReport;
}
