import React from 'react';
import { 
  HelpCircle, 
  XCircle, 
  ShieldCheck, 
  ArrowRight,
  Scale
} from 'lucide-react';
import { DashboardData } from '@/types';

interface WhyNotTabProps {
  data: DashboardData;
  onNavigateTab: (tabId: string) => void;
}

export default function WhyNotTab({ data, onNavigateTab }: WhyNotTabProps) {
  const topRec = data.recommendations[0];
  const whyNotList = topRec?.whyNotAlternatives || [];

  return (
    <div className="space-y-6">
      
      {/* Header Info */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-200 pb-4">
        <div>
          <h2 className="text-xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
            <HelpCircle className="w-5 h-5 text-teal-600" />
            Why Not? — Rejected Alternatives Analysis
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Transparent justification explaining why plausible candidate standards were disqualified in favor of the primary standard.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold px-2.5 py-1 bg-slate-100 text-slate-700 rounded-md border border-slate-200 flex items-center gap-1.5">
            <Scale className="w-3.5 h-3.5" />
            Explanatory Decision Support
          </span>
        </div>
      </div>

      {/* Primary Selection Spotlight */}
      <div className="bg-emerald-50 border border-emerald-200 rounded-xl p-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-emerald-600 text-white flex items-center justify-center font-bold text-xs shrink-0">
            WIN
          </div>
          <div>
            <div className="text-xs font-bold text-emerald-900">
              Selected Primary Benchmark: {topRec?.isNumber}
            </div>
            <div className="text-xs text-emerald-700">
              Highest requirement coverage (91% confidence) across mechanical shock and dielectric proof thresholds.
            </div>
          </div>
        </div>
        <button
          onClick={() => onNavigateTab('recommendations')}
          className="text-xs font-bold text-emerald-900 hover:underline shrink-0"
        >
          View Full Record &rarr;
        </button>
      </div>

      {/* Alternatives Disqualification Cards */}
      <div className="space-y-4">
        <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider">
          Disqualified Candidate Standards ({whyNotList.length})
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {whyNotList.map((alt, idx) => (
            <div 
              key={idx}
              className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm hover:border-slate-300 transition-all flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="inline-flex items-center gap-1 text-[11px] font-bold text-rose-700 bg-rose-50 px-2 py-0.5 rounded border border-rose-200">
                    <XCircle className="w-3 h-3 text-rose-600" />
                    Rejected Alternative
                  </span>
                  <span className="text-xs font-bold text-slate-400">
                    {alt.confidence}% Sim.
                  </span>
                </div>

                <h4 className="text-base font-extrabold text-slate-900 mt-2">
                  {alt.isNumber}
                </h4>
                <div className="text-xs font-semibold text-slate-600 mt-0.5">
                  {alt.title}
                </div>

                <div className="mt-4 p-3 bg-slate-50 rounded-lg border border-slate-100 text-xs text-slate-700 leading-relaxed">
                  <strong className="text-slate-900 block mb-1">Disqualification Rationale:</strong>
                  {alt.reason}
                </div>
              </div>

              <div className="mt-4 pt-3 border-t border-slate-100 text-[11px] text-slate-400 flex items-center justify-between">
                <span>Domain Boundary Check</span>
                <span className="font-semibold text-slate-600">Disqualified</span>
              </div>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
}
