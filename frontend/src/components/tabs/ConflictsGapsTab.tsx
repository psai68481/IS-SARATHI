import React from 'react';
import { 
  AlertTriangle, 
  HelpCircle, 
  ShieldAlert, 
  CheckCircle2, 
  Info,
  ArrowRight
} from 'lucide-react';
import { DashboardData } from '@/types';

interface ConflictsGapsTabProps {
  data: DashboardData;
  onNavigateTab: (tabId: string) => void;
}

export default function ConflictsGapsTab({ data, onNavigateTab }: ConflictsGapsTabProps) {
  const conflicts = data.conflicts || [];
  const gaps = data.gaps || [];

  return (
    <div className="space-y-6">
      
      {/* Header Info */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-200 pb-4">
        <div>
          <h2 className="text-xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-amber-500" />
            Compliance Conflicts & Specification Gaps
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Automated detection of contradictory parameters, thermal/mechanical limit violations, and missing testing clauses.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs font-bold px-2.5 py-1 bg-amber-50 text-amber-800 rounded-md border border-amber-200">
            {conflicts.length} Conflict &bull; {gaps.length} Gaps Flagged
          </span>
        </div>
      </div>

      {/* Conflicts Section */}
      <div className="space-y-4">
        <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider flex items-center gap-2">
          <ShieldAlert className="w-4 h-4 text-amber-600" />
          Technical Conflict Warnings ({conflicts.length})
        </h3>

        {conflicts.map((conf, idx) => (
          <div 
            key={idx}
            className="bg-white rounded-xl border-l-4 border-l-amber-500 border border-slate-200 p-5 shadow-sm space-y-3"
          >
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-amber-50 border border-amber-200 text-amber-800 text-xs font-bold">
                <AlertTriangle className="w-3.5 h-3.5 text-amber-600" />
                {conf.severity}
              </span>
              <span className="text-xs text-slate-400">
                Rule ID: SPEC-CONFLICT-T01
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-1">
              <div className="bg-slate-50 p-3 rounded-lg border border-slate-200">
                <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-0.5">
                  Tender Specification Stated
                </span>
                <span className="text-xs font-bold text-slate-800">
                  {conf.tenderSpec}
                </span>
              </div>

              <div className="bg-rose-50/50 p-3 rounded-lg border border-rose-200">
                <span className="text-[10px] font-bold text-rose-800 uppercase tracking-wider block mb-0.5">
                  Standard Rated Threshold
                </span>
                <span className="text-xs font-bold text-rose-900">
                  {conf.standardSpec}
                </span>
              </div>
            </div>

            <div className="bg-slate-50 p-3 rounded-lg text-xs text-slate-700 leading-relaxed border border-slate-100">
              <strong className="text-slate-900">Engineering Impact: </strong>
              {conf.impact}
            </div>

            <div className="flex items-center justify-between pt-2 text-xs">
              <span className="text-slate-500 italic">
                Recommendation: Seek amendment from tender committee or stipulate aerospace-grade heat stabilizer.
              </span>
              <button 
                onClick={() => onNavigateTab('learning')}
                className="font-bold text-teal-700 hover:underline"
              >
                Log Officer Override &rarr;
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Gaps Section */}
      <div className="space-y-4 pt-2">
        <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider flex items-center gap-2">
          <Info className="w-4 h-4 text-blue-600" />
          Omitted Requirements & Gaps ({gaps.length})
        </h3>

        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm space-y-3">
          <p className="text-xs text-slate-500 leading-relaxed">
            The following parameters were identified as critical for high-voltage industrial safety under BIS guidelines, but were omitted from the tender scope:
          </p>

          <div className="space-y-2">
            {gaps.map((gap, idx) => (
              <div key={idx} className="flex items-start gap-3 p-3 rounded-lg bg-slate-50 border border-slate-200 text-xs text-slate-700">
                <span className="w-5 h-5 rounded-full bg-blue-100 text-blue-800 flex items-center justify-center font-bold text-[11px] shrink-0 mt-0.5">
                  {idx + 1}
                </span>
                <span className="leading-relaxed">{gap}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

    </div>
  );
}
