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
}
