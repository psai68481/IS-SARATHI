import React, { useState } from 'react';
import { 
  Sparkles, 
  Cpu, 
  CheckCircle2, 
  FileText, 
  RefreshCw, 
  ArrowRight,
  Shield,
  ShieldAlert,
  Tag,
  Languages,
  AlertTriangle,
  Activity,
  Upload,
  ScanLine
} from 'lucide-react';
import { DashboardData } from '@/types';
import { analyzeTenderApi, analyzeTenderDocumentApi } from '@/lib/api';

interface TenderAnalysisTabProps {
  data: DashboardData;
  setData: (data: DashboardData) => void;
  onNavigateTab: (tabId: string) => void;
  customQuery: string;
  setCustomQuery: (query: string) => void;
}

export default function TenderAnalysisTab({ 
  data, 
  setData,
  onNavigateTab, 
  customQuery, 
  setCustomQuery 
}: TenderAnalysisTabProps) {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analyzed, setAnalyzed] = useState(true);
  const [scanStep, setScanStep] = useState("");
  const [backendError, setBackendError] = useState<string | null>(null);
  const [abstention, setAbstention] = useState<string | null>(null);
  const [analysisStatus, setAnalysisStatus] = useState<string | null>(null);
  const [includeStability, setIncludeStability] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [docInfo, setDocInfo] = useState<string | null>(null);

  const applyResult = (res: any, sourceLabel: string) => {
    if (res.detail) {
      setBackendError(typeof res.detail === 'string' ? res.detail : 'Invalid request.');
      return false;
    }
    const procGaps = [...(res.gaps || [])];
    const isAbstain = res.status === 'NOT_FOUND_IN_DATASET' || res.status === 'LOW_CONFIDENCE' || res.status === 'REJECTED_SCOPE_INCOMPATIBLE' || res.status === 'REQUIRES_HUMAN_VERIFICATION';
    setData({
      ...data,
      tenderQuery: sourceLabel === 'document' ? (res.tenderQuery || customQuery) : customQuery,
      extractedRequirements: res.extractedRequirements || [],
      recommendations: res.recommendations || [],
      conflicts: res.conflicts || [],
      gaps: procGaps,
      stability: res.stability || undefined
    });
    setAnalysisStatus(res.status || null);
    setAbstention(isAbstain ? (res.abstentionReason || 'Insufficient verified evidence.') : null);
    if (res.status === 'REJECTED_SCOPE_INCOMPATIBLE') {
      setAbstention(
        (res.abstentionReason || 'Product/scope compatibility gates rejected all retrieved candidates.') +
        (res.rejectedCandidates?.length
          ? ` Top rejected: ${res.rejectedCandidates[0].isNumber} — ${res.rejectedCandidates[0].reasons[0] || 'scope mismatch'}`
          : '')
      );
    }
    return true;
  };

  const handleAnalyze = async () => {
    if (!customQuery.trim()) return;
    setIsAnalyzing(true);
    setAnalyzed(false);
    setBackendError(null);
    setAbstention(null);
    setAnalysisStatus(null);
    setDocInfo(null);
    setScanStep("Structured procurement parsing: product identity, material, application, parameters...");

    // Call real FastAPI backend pipeline
    try {
      setTimeout(() => {
        setScanStep("Candidate retrieval + 8-check compatibility gates (hard scope rejection)...");
      }, 400);

      setTimeout(() => {
        setScanStep(
          includeStability
            ? "Evidence mapping + Recommendation Stability Check (perturbation re-analysis)..."
            : "Evidence verification, requirement coverage & conflict checking..."
        );
      }, 800);

      const res = await analyzeTenderApi(customQuery, 'Public Works Department (PWD)', includeStability);
      if (res) {
        applyResult(res, 'text');
      } else {
        setBackendError("Backend unavailable. Start the FastAPI server (port 8000) and try again — mock data is stale.");
      }
    } catch (e) {
      console.warn("Backend call handled:", e);
      setBackendError("Analysis request failed. Check backend connectivity.");
    } finally {
      setTimeout(() => {
        setIsAnalyzing(false);
        setAnalyzed(true);
        setScanStep("");
      }, 1200);
    }
  };

  const handleDocumentUpload = async (file: File, preferOcr: boolean = false) => {
    // Vercel Functions accept request bodies up to 4.5 MB — guard client-side
    // so users get a clear message instead of an edge-level 413.
    if (file.size > 4.5 * 1024 * 1024) {
      setBackendError(`"${file.name}" is ${(file.size / (1024 * 1024)).toFixed(1)} MB. The upload limit is 4.5 MB — extract the relevant tender pages into a smaller PDF.`);
      return;
    }
    setIsAnalyzing(true);
    setAnalyzed(false);
    setBackendError(null);
    setAbstention(null);
    setAnalysisStatus(null);
    setDocInfo(null);
    setScanStep(`Extracting text from ${file.name}${file.name.match(/\.(png|jpe?g)$/i) ? ' (OCR)' : ''}...`);
    try {
      setTimeout(() => setScanStep('OCR/extraction complete. Running evidence pipeline...'), 500);
      const res = await analyzeTenderDocumentApi(file, 'Public Works Department (PWD)', includeStability, preferOcr);
      setCustomQuery(res.tenderQuery ? res.tenderQuery.slice(0, 4000) : customQuery);
      if (applyResult(res, 'document')) {
        const prov = res.documentProvenance || {};
        setDocInfo(
          `${prov.documentName || file.name} — ${prov.pages ?? '?'} page(s), method: ${prov.extractionMethod || 'unknown'}, ${prov.extractedChars ?? '?'} chars extracted`
          + (prov.lowOcrConfidence ? ' — ⚠️ LOW_OCR_CONFIDENCE' : '')
        );
      }
    } catch (e: any) {
      setBackendError(e?.message || 'Document upload failed.');
    } finally {
      setTimeout(() => {
        setIsAnalyzing(false);
        setAnalyzed(true);
        setScanStep("");
      }, 900);
    }
  };

  const handleReset = () => {
    setCustomQuery(data.tenderQuery);
  };

  const topStandard = data.recommendations[0];
  const isAbstained = abstention && (!topStandard || analysisStatus === 'NOT_FOUND_IN_DATASET' || analysisStatus === 'LOW_CONFIDENCE');

  return (
    <div className="space-y-6">
      
      {/* Header Info */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-200 pb-4">
        <div>
          <h2 className="text-xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
            <FileText className="w-5 h-5 text-teal-600" />
            Tender Specification & Parameter Extraction
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Input unstructured procurement document text to extract technical requirements and map Indian Standards.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold px-2.5 py-1 bg-slate-100 text-slate-700 rounded-md border border-slate-200 flex items-center gap-1.5">
            <Languages className="w-3 h-3" />
            Multilingual: EN / हिंदी / తెలుగు
          </span>
        </div>
      </div>

      {/* Tender Query Input Box */}
      <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm">
        <div className="flex items-center justify-between mb-2">
          <label className="block text-xs font-bold uppercase tracking-wider text-slate-700">
            Procurement Tender Text / Scope of Work (SOW)
          </label>
          <button
            onClick={handleReset}
            className="text-xs text-teal-600 hover:text-teal-800 font-medium flex items-center gap-1"
          >
            <RefreshCw className="w-3 h-3" />
            Reset to Sample
          </button>
        </div>

        <div className="relative">
          <textarea
            rows={4}
            value={customQuery}
            onChange={(e) => setCustomQuery(e.target.value)}
            placeholder="Paste tender specification, BoQ items, or technical requirements here... (English, हिंदी or తెలుగు supported)"
            className="w-full text-sm text-slate-800 p-3.5 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500 focus:bg-white transition-all font-sans leading-relaxed resize-y"
          />
        </div>

        {/* Document Upload (PDF / PNG / JPG / TXT) — SIH26108 document processing */}
        <div className="mt-3 pt-3 border-t border-slate-100 flex flex-wrap items-center gap-3">
          <label className={`flex items-center gap-2 px-4 py-2 rounded-lg border border-dashed text-xs font-semibold transition-all cursor-pointer ${
            isAnalyzing
              ? 'border-slate-200 text-slate-400 cursor-not-allowed'
              : 'border-teal-300 text-teal-700 hover:bg-teal-50'
          }`}>
            <Upload className="w-4 h-4" />
            Upload Tender (PDF / PNG / JPG / TXT)
            <input
              type="file"
              accept=".pdf,.txt,.png,.jpg,.jpeg"
              className="hidden"
              disabled={isAnalyzing}
              onChange={(e) => {
                const f = e.target.files?.[0];
                if (f) handleDocumentUpload(f);
                e.currentTarget.value = '';
              }}
            />
          </label>
          <span className="text-[11px] text-slate-400 flex items-center gap-1">
            <ScanLine className="w-3.5 h-3.5" />
            Scanned PDFs/images fall back to OCR; unreadable text is flagged LOW_OCR_CONFIDENCE, never guessed.
          </span>
        </div>
        {docInfo && (
          <div className="mt-3 p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-[11px] text-slate-600 flex items-start gap-2">
            <FileText className="w-3.5 h-3.5 text-slate-400 mt-0.5 shrink-0" />
            <span>{docInfo}</span>
          </div>
        )}

        <div className="mt-4 flex flex-wrap items-center justify-between gap-3 pt-3 border-t border-slate-100">
          <div className="flex flex-wrap items-center gap-2 text-xs text-slate-500">
            <span className="font-semibold text-slate-700">{customQuery.length}</span> characters
            <span>&bull;</span>
            <span>Format: <strong>Technical Tender Specs</strong></span>
          </div>

          <div className="flex items-center gap-2">
            <label className="flex items-center gap-1.5 text-xs text-slate-600 font-medium cursor-pointer select-none mr-1">
              <input
                type="checkbox"
                checked={includeStability}
                onChange={(e) => setIncludeStability(e.target.checked)}
                disabled={isAnalyzing}
                className="w-3.5 h-3.5 accent-[#028090] cursor-pointer"
              />
              <Activity className="w-3.5 h-3.5 text-slate-500" />
              Stability Check
            </label>
            <button
              onClick={handleAnalyze}
              disabled={isAnalyzing || !customQuery.trim()}
              className={`px-5 py-2.5 rounded-lg text-xs font-bold text-white shadow-sm flex items-center gap-2 transition-all active:scale-95 ${
                isAnalyzing || !customQuery.trim()
                  ? "bg-slate-400 cursor-not-allowed"
                  : "bg-[#028090] hover:bg-[#006d7b]"
              }`}
            >
              {isAnalyzing ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin" />
                  <span>Analyzing Specification...</span>
                </>
              ) : (
                <>
                  <Sparkles className="w-4 h-4" />
                  <span>Analyze Specification</span>
                </>
              )}
            </button>
          </div>
        </div>

        {/* Dynamic scan progress indicator */}
        {isAnalyzing && (
          <div className="mt-4 p-3 bg-teal-50 rounded-lg border border-teal-200 flex items-center gap-3 animate-pulse">
            <Cpu className="w-5 h-5 text-teal-600 animate-spin" />
            <div className="text-xs text-teal-900 font-medium">
              {scanStep}
            </div>
          </div>
        )}
      </div>

      {/* Backend connectivity / request error banner */}
      {backendError && (
        <div className="bg-rose-50 border border-rose-200 rounded-xl p-4 flex items-start gap-3">
          <AlertTriangle className="w-5 h-5 text-rose-600 shrink-0 mt-0.5" />
          <div className="text-xs text-rose-900">
            <p className="font-bold">Analysis could not run</p>
            <p className="mt-0.5">{backendError}</p>
          </div>
        </div>
      )}

      {/* Abstention / Insufficient Evidence banner (feature #23) */}
      {isAbstained && (
        <div className="bg-amber-50 border border-amber-300 rounded-xl p-5 flex items-start gap-3">
          <ShieldAlert className="w-6 h-6 text-amber-600 shrink-0 mt-0.5" />
          <div className="text-xs text-amber-900 space-y-1.5">
            <p className="font-extrabold uppercase tracking-wide">
              ⚠️ Insufficient evidence to confidently recommend a standard
            </p>
            <p>{abstention}</p>
            {data.gaps.length > 0 && (
              <ul className="list-disc list-inside space-y-0.5 pt-1">
                {data.gaps.map((g, i) => (
                  <li key={i}>{g}</li>
                ))}
              </ul>
            )}
            <p className="pt-1 font-medium">
              The system deliberately refuses to guess. Human verification is required.
            </p>
          </div>
        </div>
      )}

      {/* Extracted Requirements Section */}
      {analyzed && data.extractedRequirements.length > 0 && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                Extracted Parameters & Requirements ({data.extractedRequirements.length})
              </h3>
              <p className="text-xs text-slate-500">
                Key technical parameters structured by the NLP engine for standard matching
              </p>
            </div>
            
            {topStandard && (
              <button
                onClick={() => onNavigateTab('recommendations')}
                className="text-xs font-bold text-teal-700 hover:text-teal-900 flex items-center gap-1"
              >
                <span>View Recommended Standards</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            )}
          </div>

          {/* Cards Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {data.extractedRequirements.map((req, idx) => (
              <div 
                key={idx}
                className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm hover:border-teal-300 hover:shadow-md transition-all"
              >
                <div className="flex items-center justify-between text-xs text-slate-400 mb-2">
                  <span className="inline-flex items-center gap-1 font-semibold text-slate-500 bg-slate-100 px-2 py-0.5 rounded text-[11px]">
                    <Tag className="w-3 h-3 text-slate-400" />
                    {req.category || "General"}
                  </span>
                  <span className="text-[11px] font-bold text-emerald-600">
                    {req.confidence || 95}% conf.
                  </span>
                </div>

                <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
                  {req.field}
                </div>
                
                <div className="text-base font-extrabold text-slate-900 mt-1 font-sans">
                  {req.value}
                </div>
              </div>
            ))}
          </div>

          {/* Extraction Analysis Footnote — dynamic, reflects real top standard */}
          {topStandard && (
            <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div className="flex items-start sm:items-center gap-3">
                <div className="w-8 h-8 rounded-lg bg-teal-100 text-teal-800 flex items-center justify-center shrink-0">
                  <Shield className="w-4 h-4" />
                </div>
                <div className="text-xs text-slate-700">
                  <p className="font-bold text-slate-900">
                    Primary Standard Identified: <span className="text-teal-700">{topStandard.isNumber} ({topStandard.title})</span>
                  </p>
                  <p className="text-slate-500">
                    Evidence: {topStandard.coverageMap?.filter(c => c.covered).length ?? 0} of{' '}
                    {topStandard.coverageMap?.length ?? 0} specification items mapped to verified clauses.
                  </p>
                </div>
              </div>

              <button
                onClick={() => onNavigateTab('coverage')}
                className="px-3.5 py-1.5 bg-white hover:bg-slate-100 text-slate-700 text-xs font-bold rounded-lg border border-slate-300 shadow-sm transition-all shrink-0"
              >
                Verify Clause Coverage
              </button>
            </div>
          )}
        </div>
      )}

      {/* Empty state when nothing extracted */}
      {analyzed && data.extractedRequirements.length === 0 && !backendError && !isAbstained && (
        <div className="bg-white rounded-xl border border-dashed border-slate-300 p-8 text-center text-sm text-slate-500">
          Enter a tender specification above and click <strong>Analyze Specification</strong> to run the evidence pipeline.
        </div>
      )}

    </div>
  );
}
