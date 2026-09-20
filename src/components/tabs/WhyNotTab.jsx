import React from 'react';
import { 
  HelpCircle, 
  XCircle, 
  Sparkles, 
  FilterX, 
  AlertCircle 
} from 'lucide-react';
import ConfidenceBadge from '../common/ConfidenceBadge';

export default function WhyNotTab({ data, onNavigateTab }) {
  const recommendations = data.recommendations || [];
  const topRec = recommendations[0];
  const alternatives = topRec?.whyNotAlternatives || [];

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-200 pb-4">
        <div>
          <h2 className="text-xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
            <HelpCircle className="w-5 h-5 text-teal-600" />
            AI Disqualification Rationale ("Why Not?")
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Transparent explainability showing why plausible Indian Standards were rejected or ranked lower during candidate evaluation.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold px-2.5 py-1 bg-slate-100 text-slate-700 rounded-md border border-slate-200">
            {alternatives.length} Alternatives Disqualified
          </span>
        </div>
      </div>

      {/* Rationale Overview Box */}
      <div className="bg-slate-100/80 rounded-xl p-4 border border-slate-200 flex items-start gap-3 text-xs text-slate-700">
        <FilterX className="w-5 h-5 text-slate-500 shrink-0 mt-0.5" />
        <div>
          <span className="font-bold text-slate-900">Explainable AI Filtering: </span>
          The vector retriever initially matched multiple candidate standards across domains. Below is the decision rationale for why candidates were disqualified
          {topRec?.isNumber ? (
            <> in favor of <strong className="text-teal-700">{topRec.isNumber}</strong>.</>
          ) : (
            <> due to scope incompatibility with the detected procurement requirement.</>
          )}
        </div>
      </div>

      {/* Disqualified Alternatives Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {alternatives.map((alt, idx) => (
          <div
            key={idx}
            className="bg-slate-100/60 rounded-xl border border-slate-300/80 p-5 shadow-sm hover:bg-slate-100 transition-all flex flex-col justify-between relative overflow-hidden group"
          >
            {/* Strikethrough visual accent on top-right */}
            <div className="absolute top-0 right-0 bg-slate-200 text-slate-500 text-[10px] font-extrabold uppercase tracking-widest px-3 py-1 rounded-bl-lg border-l border-b border-slate-300 flex items-center gap-1">
              <XCircle className="w-3 h-3 text-rose-500" />
              <span>Disqualified</span>
            </div>

            <div className="space-y-3">
              {/* IS Number with Strikethrough */}
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-lg font-black text-slate-500 line-through decoration-rose-500 decoration-2 font-mono">
                    {alt.isNumber}
                  </span>
                </div>
                {alt.title && (
                  <div className="text-xs font-bold text-slate-700 mt-1">
                    {alt.title}
                  </div>
                )}
              </div>

              {/* Confidence Score Pill */}
              <div className="flex items-center justify-between text-xs">
                <span className="text-slate-400 font-medium">Confidence Score:</span>
                <ConfidenceBadge score={alt.confidence} size="sm" />
              </div>

              {/* Disqualification Reason */}
              <div className="p-3 bg-white/90 rounded-lg border border-slate-200/90 text-xs text-slate-700 leading-relaxed">
                <span className="font-bold text-slate-900 block mb-1 flex items-center gap-1">
                  <AlertCircle className="w-3.5 h-3.5 text-rose-500 shrink-0" />
                  Rejection Reason:
                </span>
                {alt.reason}
              </div>
            </div>

            {/* Bottom Meta */}
            <div className="mt-4 pt-3 border-t border-slate-200 flex items-center justify-between text-[11px] text-slate-400">
              <span>Decision: Rejected at Step 2</span>
              <span className="text-slate-500 font-mono">Rank #{idx + 2}</span>
            </div>

          </div>
        ))}
      </div>

      {/* Bottom Tip for Procurement Auditor */}
      <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs">
        <div className="flex items-center gap-2.5 text-slate-600">
          <Sparkles className="w-4 h-4 text-teal-600 shrink-0" />
          <span>
            Need to reconsider a disqualified candidate? You can manually override in the <strong>AI Override & Learning</strong> panel.
          </span>
        </div>

        <button
          onClick={() => onNavigateTab('learning')}
          className="px-3.5 py-1.5 bg-[#028090] hover:bg-[#006d7b] text-white text-xs font-bold rounded-lg shadow-sm transition-all shrink-0"
        >
          View Override Audit
        </button>
      </div>

    </div>
  );
}
