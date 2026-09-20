import React from 'react';
import { 
  Bot, 
  Award, 
  Bookmark, 
  CheckCircle2, 
  AlertTriangle, 
  ArrowRight, 
  Sparkles, 
  FileCheck2, 
  Calendar, 
  FileEdit, 
  ShieldCheck, 
  Layers,
  ChevronRight
} from 'lucide-react';
import ConfidenceGauge from '../common/ConfidenceGauge';
import ConfidenceBadge from '../common/ConfidenceBadge';
import { StandardTypeBadge, StatusBadge, CertificationBadge } from '../common/StatusBadge';

export default function RecommendationsTab({ data, onNavigateTab }) {
  const recommendations = data.recommendations || [];

  if (recommendations.length === 0) {
    return (
      <div className="space-y-6">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-200 pb-4">
          <div>
            <h2 className="text-xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
              <Bot className="w-5 h-5 text-amber-600" />
              AI Indian Standards Recommendations
            </h2>
            <p className="text-xs text-slate-500 mt-0.5">
              Ranked standard recommendations generated from semantic specification matching and BIS gazette compliance.
            </p>
          </div>
          <div className="flex items-center gap-2 text-xs">
            <span className="font-semibold text-rose-800 bg-rose-50 px-2.5 py-1 rounded-md border border-rose-200">
              NOT FOUND IN DATASET
            </span>
          </div>
        </div>

        {/* Not Found in Dataset Card */}
        <div className="bg-amber-50/70 border-2 border-amber-400 rounded-2xl p-6 sm:p-8 space-y-4 shadow-xs">
          <div className="flex items-start gap-4">
            <div className="p-3 bg-amber-100 text-amber-800 rounded-xl shrink-0 mt-0.5">
              <AlertTriangle className="w-6 h-6" />
            </div>
            <div className="space-y-2">
              <h3 className="text-lg font-extrabold text-amber-950">
                NO APPLICABLE STANDARD FOUND IN CURRENT DATASET
              </h3>
              <p className="text-xs sm:text-sm text-amber-900 leading-relaxed font-medium">
                The requested procurement requirement is not covered by the current IS-SARATHI knowledge base.
              </p>
              <p className="text-xs text-amber-800 italic">
                {data.abstentionReason}
              </p>
              <div className="pt-2 text-xs text-amber-800 space-y-1">
                <p className="font-bold">Recommended Action:</p>
                <ul className="list-disc list-inside space-y-0.5 text-amber-900">
                  <li>Human verification / official BIS e-Sale portal search recommended.</li>
                  <li>Check if standard is cataloged under alternate product nomenclatures.</li>
                  <li>Verify if new gazette Quality Control Orders (QCO) apply to this material category.</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  const primaryRec = recommendations.find(r => r.type === "Primary Standard") || recommendations[0];
  const relatedRecs = recommendations.filter(r => r.isNumber !== primaryRec.isNumber);

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-200 pb-4">
        <div>
          <h2 className="text-xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
            <Bot className="w-5 h-5 text-teal-600" />
            AI Indian Standards Recommendations
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Ranked standard recommendations generated from semantic specification matching and BIS gazette compliance.
          </p>
        </div>
        <div className="flex items-center gap-2 text-xs">
          <span className="font-semibold text-slate-700 bg-teal-50 text-teal-800 px-2.5 py-1 rounded-md border border-teal-200">
            {recommendations.length} Standards Matched
          </span>
        </div>
      </div>

      {/* Featured Primary Recommendation Card (Larger / Highlighted) */}
      <div className="relative bg-white rounded-2xl border-2 border-teal-500/80 shadow-md p-6 sm:p-7 overflow-hidden">
        {/* Accent top ribbon */}
        <div className="absolute top-0 left-0 right-0 h-1.5 bg-gradient-to-r from-teal-600 via-teal-400 to-blue-600" />
        
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
          
          {/* Left / Center Info */}
          <div className="space-y-4 flex-1">
            
            {/* Badges Row */}
            <div className="flex flex-wrap items-center gap-2">
              <StandardTypeBadge type={primaryRec.type} />
              <StatusBadge status={primaryRec.status} />
              <CertificationBadge certification={primaryRec.certification} />
              <span className="text-xs font-semibold px-2 py-0.5 rounded bg-slate-100 text-slate-600 border border-slate-200">
                {primaryRec.category}
              </span>
            </div>

            {/* Standard IS Title & Number */}
            <div>
              <div className="flex items-baseline gap-3 flex-wrap">
                <h3 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight font-sans">
                  {primaryRec.isNumber}
                </h3>
                <span className="text-xs font-bold text-teal-600 bg-teal-50 px-2.5 py-0.5 rounded-full border border-teal-200">
                  Recommended Primary Baseline
                </span>
              </div>
              <h4 className="text-base sm:text-lg font-bold text-slate-700 mt-1">
                {primaryRec.title}
              </h4>
              <p className="text-xs text-slate-600 mt-2 leading-relaxed max-w-3xl">
                {primaryRec.description}
              </p>
            </div>

            {/* Version & Amendment Meta Strip */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
              <div className="bg-slate-50 p-3 rounded-lg border border-slate-200">
                <div className="text-[11px] font-bold text-slate-500 uppercase tracking-wide flex items-center gap-1.5">
                  <Calendar className="w-3.5 h-3.5 text-slate-400" />
                  Latest Valid Version
                </div>
                <div className="text-xs font-bold text-slate-800 mt-0.5">
                  {primaryRec.latestVersion}
                </div>
              </div>

              <div className="bg-slate-50 p-3 rounded-lg border border-slate-200">
                <div className="text-[11px] font-bold text-slate-500 uppercase tracking-wide flex items-center gap-1.5">
                  <FileEdit className="w-3.5 h-3.5 text-slate-400" />
                  Gazette Amendment
                </div>
                <div className="text-xs font-medium text-slate-800 mt-0.5">
                  {primaryRec.amendment}
                </div>
              </div>
            </div>

            {/* Key Clauses Preview */}
            {primaryRec.keyClauses && (
              <div className="pt-2">
                <span className="text-[11px] font-bold text-slate-500 uppercase tracking-wide">
                  Key Verification Clauses in Standard:
                </span>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 mt-1.5">
                  {primaryRec.keyClauses.map((c, i) => (
                    <div key={i} className="flex items-center gap-2 text-xs text-slate-700 bg-slate-50/80 px-2.5 py-1.5 rounded border border-slate-200">
                      <span className="font-bold text-teal-700">{c.clause}:</span>
                      <span className="truncate text-slate-600">{c.title}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

          </div>

          {/* Right Column: Circular Gauge & Quick Navigation */}
          <div className="lg:w-60 flex flex-col items-center justify-between border-t lg:border-t-0 lg:border-l border-slate-200 pt-6 lg:pt-0 lg:pl-6 shrink-0">
            
            <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200 w-full flex flex-col items-center">
              <ConfidenceGauge 
                score={primaryRec.confidence} 
                size={120} 
                strokeWidth={10} 
                label="AI Match Confidence" 
              />
              <div className="mt-2 text-center">
                <span className={`text-xs font-bold px-2.5 py-0.5 rounded-full border ${
                  primaryRec.confidence >= 85 
                    ? "text-emerald-600 bg-emerald-50 border-emerald-200" 
                    : primaryRec.confidence >= 70 
                      ? "text-amber-600 bg-amber-50 border-amber-200" 
                      : "text-rose-600 bg-rose-50 border-rose-200"
                }`}>
                  {primaryRec.evidenceTier || (primaryRec.confidence >= 85 ? "HIGH EVIDENCE" : primaryRec.confidence >= 70 ? "MEDIUM EVIDENCE" : "LOW EVIDENCE — Verify")}
                </span>
              </div>
            </div>

            <div className="w-full space-y-2 mt-4">
              <button
                onClick={() => onNavigateTab('related-standards')}
                className="w-full py-2 px-3 bg-teal-600 hover:bg-teal-700 text-white rounded-lg text-xs font-bold shadow-xs transition-all flex items-center justify-between"
              >
                <span>View Related Standards Tree</span>
                <ChevronRight className="w-4 h-4" />
              </button>

              <button
                onClick={() => onNavigateTab('coverage')}
                className="w-full py-2 px-3 bg-slate-100 hover:bg-slate-200 text-slate-800 rounded-lg text-xs font-semibold transition-all flex items-center justify-between"
              >
                <span>Clause Coverage Matrix</span>
                <ChevronRight className="w-4 h-4 text-slate-400" />
              </button>
            </div>

          </div>

        </div>
      </div>

      {/* Related / Secondary Recommendation Cards */}
      <div className="space-y-4">
        <h3 className="text-sm font-bold uppercase tracking-wider text-slate-500">
          Secondary & Harmonized Standards ({relatedRecs.length})
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {relatedRecs.map((rec, idx) => (
            <div 
              key={idx}
              className="bg-white rounded-xl border border-slate-200 p-5 shadow-xs hover:border-slate-300 transition-all flex flex-col justify-between"
            >
              <div className="space-y-3">
                {/* Top Badges & Confidence Score */}
                <div className="flex items-center justify-between gap-2">
                  <div className="flex items-center gap-2 flex-wrap">
                    <StandardTypeBadge type={rec.type} />
                    <StatusBadge status={rec.status} />
                  </div>
                  <ConfidenceBadge score={rec.confidence} size="sm" />
                </div>

                {/* Title */}
                <div>
                  <h4 className="text-lg font-bold text-slate-900 font-sans">
                    {rec.isNumber}
                  </h4>
                  <div className="text-xs font-semibold text-slate-700 mt-0.5">
                    {rec.title}
                  </div>
                  <p className="text-xs text-slate-500 mt-2 line-clamp-2">
                    {rec.description}
                  </p>
                </div>

                {/* Meta details */}
                <div className="grid grid-cols-2 gap-2 text-xs pt-2 border-t border-slate-100">
                  <div>
                    <span className="text-slate-400 block text-[10px] font-bold uppercase">Version:</span>
                    <span className="font-semibold text-slate-700">{rec.latestVersion}</span>
                  </div>
                  <div>
                    <span className="text-slate-400 block text-[10px] font-bold uppercase">Certification:</span>
                    <span className="font-semibold text-slate-700">{rec.certification.status}</span>
                  </div>
                </div>
              </div>

              <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between">
                <span className="text-xs text-slate-500">
                  Amendment: <strong className="text-slate-700">{rec.amendment}</strong>
                </span>
                <button
                  onClick={() => onNavigateTab('related-standards')}
                  className="text-xs font-bold text-teal-600 hover:text-teal-800 flex items-center gap-1"
                >
                  <span>Explore Graph</span>
                  <ChevronRight className="w-3.5 h-3.5" />
                </button>
              </div>

            </div>
          ))}
        </div>
      </div>

    </div>
  );
}
