import React from 'react';
import { 
  Bot, 
  CheckCircle2, 
  Clock, 
  FileBadge, 
  Layers, 
  ShieldCheck, 
  ArrowRight,
  Sparkles,
  GitFork,
  HelpCircle,
  ShieldAlert,
  Activity,
  AlertTriangle,
  CheckCheck
} from 'lucide-react';
import ConfidenceBadge from '../common/ConfidenceBadge';
import StatusBadge from '../common/StatusBadge';
import { DashboardData, StabilityReport } from '@/types';

interface RecommendationsTabProps {
  data: DashboardData;
  onNavigateTab: (tabId: string) => void;
}

const STABILITY_STYLES: Record<string, { badge: string; icon: JSX.Element; label: string }> = {
  STABLE: {
    badge: "bg-emerald-50 text-emerald-800 border-emerald-200",
    icon: <CheckCheck className="w-4 h-4 text-emerald-600" />,
    label: "Stable — ranking holds under requirement perturbation",
  },
  MODERATE: {
    badge: "bg-amber-50 text-amber-800 border-amber-200",
    icon: <Activity className="w-4 h-4 text-amber-600" />,
    label: "Moderate — some requirements move the ranking",
  },
  FRAGILE: {
    badge: "bg-rose-50 text-rose-800 border-rose-200",
    icon: <AlertTriangle className="w-4 h-4 text-rose-600" />,
    label: "Fragile — ranking is highly sensitive to a specification",
  },
  NOT_APPLICABLE: {
    badge: "bg-slate-50 text-slate-600 border-slate-200",
    icon: <Activity className="w-4 h-4 text-slate-400" />,
    label: "Not applicable — no baseline recommendation to test",
  },
};

function StabilityPanel({ stability }: { stability: StabilityReport }) {
  const style = STABILITY_STYLES[stability.overall] || STABILITY_STYLES.NOT_APPLICABLE;
  return (
    <div className="mt-4 rounded-xl border border-slate-200 bg-slate-50/60 p-4">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <div className="flex items-center gap-2">
          {style.icon}
          <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700">
            Recommendation Stability Check
          </h4>
        </div>
        <span className={`text-[11px] font-bold px-2.5 py-0.5 rounded-full border ${style.badge}`}>
          {stability.overall}
        </span>
      </div>
      <p className="text-[11px] text-slate-500 mt-1.5">{style.label} — each listed requirement was removed/emphasized and the full evidence pipeline re-run.</p>

      {stability.summary.length > 0 && (
        <div className="mt-3 space-y-2">
          {stability.summary.map((item, idx) => (
            <div
              key={idx}
              className={`rounded-lg border p-2.5 text-xs ${
                item.critical
                  ? "bg-rose-50 border-rose-200"
                  : item.maxDrop >= 8
                    ? "bg-amber-50 border-amber-200"
                    : "bg-white border-slate-200"
              }`}
            >
              <div className="flex flex-wrap items-center justify-between gap-2">
                <span className="font-semibold text-slate-800">{item.requirement}</span>
                <span className="flex items-center gap-2 text-[11px]">
                  {item.critical && (
                    <span className="font-bold px-2 py-0.5 rounded-full bg-rose-600 text-white">
                      CRITICAL
                    </span>
                  )}
                  <span className={item.maxDrop > 0 ? "text-rose-700 font-bold" : "text-emerald-700 font-bold"}>
                    {item.maxDrop > 0 ? `−${item.maxDrop.toFixed(1)} pts` : "no drop"}
                  </span>
                </span>
              </div>
              <div className="text-[11px] text-slate-500 mt-1">
                &ldquo;{item.fragment}&rdquo;
                {item.flippedOnRemove && " · ranking flips when removed"}
                {item.abstainedOnRemove && " · engine abstains when removed"}
                {item.emphasizeGain > 3 && ` · +${item.emphasizeGain.toFixed(1)} pts when emphasized`}
              </div>
            </div>
          ))}
        </div>
      )}

      {stability.overall === "FRAGILE" && (
        <p className="mt-3 text-[11px] text-rose-900 font-medium flex items-start gap-1.5">
          <ShieldAlert className="w-3.5 h-3.5 shrink-0 mt-0.5" />
          {stability.note}
        </p>
      )}
    </div>
  );
}

export default function RecommendationsTab({ data, onNavigateTab }: RecommendationsTabProps) {
  const primaryRec = data.recommendations[0];
  const relatedRecs = data.recommendations.slice(1);

  if (!primaryRec) {
    return (
      <div className="space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-200 pb-4">
          <div>
            <h2 className="text-xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
              <Bot className="w-5 h-5 text-teal-600" />
              Ranked Standards Recommendations
            </h2>
            <p className="text-xs text-slate-500 mt-0.5">
              Evidence-grounded shortlist of applicable Indian Standards ranked by requirement coverage and compliance confidence.
            </p>
          </div>
        </div>

        {/* Honest abstention state — never fabricate a recommendation */}
        <div className="bg-amber-50 border border-amber-300 rounded-xl p-6 flex items-start gap-3">
          <ShieldAlert className="w-6 h-6 text-amber-600 shrink-0 mt-0.5" />
          <div className="text-xs text-amber-900 space-y-1.5">
            <p className="font-extrabold uppercase tracking-wide">
              ⚠️ No recommendation issued — insufficient verified evidence
            </p>
            {data.gaps.length > 0 ? (
              <ul className="list-disc list-inside space-y-0.5 pt-1">
                {data.gaps.map((g, i) => (
                  <li key={i}>{g}</li>
                ))}
              </ul>
            ) : (
              <p>Run a tender analysis first. The system only recommends standards backed by verified knowledge-base evidence.</p>
            )}
            <button
              onClick={() => onNavigateTab('tender-analysis')}
              className="mt-2 px-3.5 py-1.5 bg-amber-600 hover:bg-amber-700 text-white text-xs font-bold rounded-lg shadow-sm transition-all"
            >
              Go to Tender Analysis →
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      
      {/* Header Info */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-200 pb-4">
        <div>
          <h2 className="text-xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
            <Bot className="w-5 h-5 text-teal-600" />
            Ranked Standards Recommendations
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Evidence-grounded shortlist of applicable Indian Standards ranked by requirement coverage and compliance confidence.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold px-2.5 py-1 bg-emerald-50 text-emerald-700 rounded-md border border-emerald-200 flex items-center gap-1.5">
            <CheckCircle2 className="w-3.5 h-3.5" />
            Grounded in BIS Knowledge Base
          </span>
        </div>
      </div>

      {/* Primary Recommendation Card */}
      <div className="bg-white rounded-2xl border-2 border-teal-500/40 p-5 sm:p-6 shadow-md relative overflow-hidden">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 pb-4 border-b border-slate-100">
          <div>
            <div className="flex flex-wrap items-center gap-2 mb-1.5">
              <span className="bg-[#1E2761] text-white text-[11px] font-extrabold px-2.5 py-0.5 rounded uppercase tracking-wider">
                Primary Standard
              </span>
              <StatusBadge status={primaryRec.status} />
              <span className="text-xs text-slate-400 font-medium">
                Category: <strong className="text-slate-700">{primaryRec.category}</strong>
              </span>
            </div>
            <h3 className="text-lg sm:text-xl font-black text-slate-900 tracking-tight">
              {primaryRec.isNumber}: {primaryRec.title}
            </h3>
          </div>

          <div className="flex items-center gap-3">
            <ConfidenceBadge score={primaryRec.confidence} size="lg" />
          </div>
        </div>

        {/* Why Recommended — evidence-based explanation (feature #15) */}
        {primaryRec.whyRecommended && (
          <div className="mt-4 bg-teal-50/70 border border-teal-200 rounded-lg p-3.5">
            <div className="flex items-start gap-2">
              <Sparkles className="w-4 h-4 text-teal-700 mt-0.5 shrink-0" />
              <div className="text-xs text-teal-900 leading-relaxed">
                <strong className="uppercase tracking-wider text-[10px] block mb-1">Why This Standard?</strong>
                {primaryRec.whyRecommended}
              </div>
            </div>
          </div>
        )}

        {/* Scope & Applicability */}
        <div className="py-4 space-y-3">
          <div>
            <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-1">
              Standard Scope & Application
            </h4>
            <p className="text-xs sm:text-sm text-slate-700 leading-relaxed">
              {primaryRec.description}
            </p>
          </div>

          {/* Version, Amendment & Certification Details */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-2">
            <div className="bg-slate-50 p-3 rounded-lg border border-slate-200">
              <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block mb-0.5">
                Version & Reaffirmation
              </span>
              <span className="text-xs font-semibold text-slate-800 flex items-center gap-1">
                <Clock className="w-3.5 h-3.5 text-slate-400" />
                {primaryRec.latestVersion}
              </span>
            </div>

            <div className="bg-slate-50 p-3 rounded-lg border border-slate-200">
              <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block mb-0.5">
                Amendment Status
              </span>
              <span className="text-xs font-semibold text-slate-800">
                {primaryRec.amendment}
              </span>
            </div>

            <div className="bg-amber-50/60 p-3 rounded-lg border border-amber-200">
              <span className="text-[10px] font-bold uppercase tracking-wider text-amber-800 block mb-0.5">
                Certification Scheme
              </span>
              <span className="text-xs font-bold text-amber-900 flex items-center gap-1">
                <FileBadge className="w-3.5 h-3.5 text-amber-700" />
                {primaryRec.certification.scheme} ({primaryRec.certification.status})
              </span>
            </div>
          </div>
        </div>

        {/* Recommendation Stability Check (feature #24) */}
        {data.stability && <StabilityPanel stability={data.stability} />}

        {/* Key Normative Clauses Mapping */}
        {primaryRec.keyClauses.length > 0 && (
          <div className="pt-3 border-t border-slate-100">
            <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">
              Mandatory Requirement Clauses Mapped
            </h4>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
              {primaryRec.keyClauses.map((clause, idx) => (
                <div key={idx} className="flex items-center gap-2 p-2 rounded-lg bg-slate-50 border border-slate-200 text-xs">
                  <span className="font-mono font-bold text-teal-700 bg-white px-2 py-0.5 rounded border border-slate-200">
                    {clause.clause}
                  </span>
                  <span className="text-slate-700 font-medium truncate">
                    {clause.title}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Action Buttons */}
        <div className="mt-5 pt-4 border-t border-slate-100 flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-2 text-xs text-slate-500">
            <Sparkles className="w-4 h-4 text-teal-600" />
            <span>
              Coverage: <strong>{primaryRec.coverageMap?.filter(c => c.covered).length ?? 0}/{primaryRec.coverageMap?.length ?? 0}</strong> items evidenced
            </span>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => onNavigateTab('why-not')}
              className="px-3.5 py-1.5 rounded-lg border border-slate-300 text-slate-700 hover:bg-slate-100 text-xs font-semibold flex items-center gap-1.5 transition-all"
            >
              <HelpCircle className="w-3.5 h-3.5 text-slate-500" />
              <span>Why Not Alternatives?</span>
            </button>
            <button
              onClick={() => onNavigateTab('related-standards')}
              className="px-3.5 py-1.5 rounded-lg bg-teal-600 hover:bg-teal-700 text-white text-xs font-semibold flex items-center gap-1.5 shadow-sm transition-all"
            >
              <GitFork className="w-3.5 h-3.5" />
              <span>Explore Allied Standards ({primaryRec.relatedStandards.length})</span>
            </button>
          </div>
        </div>
      </div>

      {/* Alternative & Allied Candidates */}
      {relatedRecs.length > 0 && (
        <div className="space-y-3">
          <h3 className="text-sm font-bold text-slate-800 uppercase tracking-wider flex items-center gap-2">
            <Layers className="w-4 h-4 text-slate-500" />
            Allied & Complementary Standards ({relatedRecs.length})
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {relatedRecs.map((rec, idx) => (
              <div key={idx} className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm hover:border-slate-300 transition-all">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-[10px] font-bold text-slate-500 bg-slate-100 px-2 py-0.5 rounded uppercase">
                    {rec.type}
                  </span>
                  <ConfidenceBadge score={rec.confidence} size="sm" />
                </div>
                <h4 className="font-bold text-slate-900 text-sm">
                  {rec.isNumber}: {rec.title}
                </h4>
                <p className="text-xs text-slate-500 mt-1 line-clamp-2">
                  {rec.description}
                </p>
                <div className="mt-3 pt-2 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
                  <span>Version: {rec.latestVersion}</span>
                  <span className="font-semibold text-teal-600 cursor-pointer hover:underline" onClick={() => onNavigateTab('related-standards')}>
                    Details &rarr;
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

    </div>
  );
}
