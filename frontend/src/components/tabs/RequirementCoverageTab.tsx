import React from 'react';
import { 
  CheckSquare, 
  CheckCircle2, 
  XCircle, 
  AlertCircle, 
  ArrowRight,
  ShieldCheck
} from 'lucide-react';
import { DashboardData } from '@/types';

interface RequirementCoverageTabProps {
  data: DashboardData;
  onNavigateTab: (tabId: string) => void;
}

export default function RequirementCoverageTab({ data, onNavigateTab }: RequirementCoverageTabProps) {
  const topRec = data.recommendations[0];
  const coverageList = topRec?.coverageMap || [];

  const coveredCount = coverageList.filter(c => c.covered).length;
  const totalCount = coverageList.length;
  const coveragePercent = totalCount > 0 ? Math.round((coveredCount / totalCount) * 100) : 0;

  if (!topRec || totalCount === 0) {
    return (
      <div className="space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-200 pb-4">
          <div>
            <h2 className="text-xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
              <CheckSquare className="w-5 h-5 text-teal-600" />
              Requirement Coverage & Clause Mapping
            </h2>
            <p className="text-xs text-slate-500 mt-0.5">
              No verified clause coverage is available until a tender is analyzed against the IS-SARATHI corpus.
            </p>
          </div>
        </div>

        <div className="bg-white rounded-xl border border-dashed border-slate-300 p-8 text-center text-sm text-slate-500">
          Run the analysis workflow to populate clause-by-clause evidence from the verified standards database.
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
            <CheckSquare className="w-5 h-5 text-teal-600" />
            Requirement Coverage & Clause Mapping
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Cross-verifies whether every parameter in the procurement specification is explicitly backed by an authoritative clause.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs font-bold px-3 py-1 bg-teal-50 text-teal-800 rounded-lg border border-teal-200">
            {coveredCount} of {totalCount} Requirements Covered ({coveragePercent}%)
          </span>
        </div>
      </div>

      {/* Overview Progress Meter */}
      <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="text-xs font-bold uppercase tracking-wider text-slate-400">
            Current Standard Coverage Score
          </div>
          <div className="text-2xl font-black text-slate-900 font-sans">
            {topRec?.isNumber} &bull; {coveragePercent}% Verified
          </div>
          <p className="text-xs text-slate-500">
            Evidence-backed clause alignment is shown below for the currently selected recommendation. Review unmatched items with the procurement authority before release.
          </p>
        </div>

        <div className="w-full sm:w-64 space-y-1.5">
          <div className="flex justify-between text-xs font-bold">
            <span className="text-slate-600">Clause Alignment</span>
            <span className="text-teal-700">{coveragePercent}%</span>
          </div>
          <div className="w-full h-3 bg-slate-100 rounded-full overflow-hidden border border-slate-200">
            <div 
              className="h-full bg-gradient-to-r from-teal-500 to-emerald-500 rounded-full transition-all duration-500"
              style={{ width: `${coveragePercent}%` }}
            />
          </div>
        </div>
      </div>

      {/* Coverage Table */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs sm:text-sm border-collapse">
            <thead className="bg-slate-50 text-slate-600 font-bold border-b border-slate-200 text-xs uppercase tracking-wider">
              <tr>
                <th className="p-3.5">Status</th>
                <th className="p-3.5">Tender Parameter</th>
                <th className="p-3.5">Standard Evidence</th>
                <th className="p-3.5">Verification Finding</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {coverageList.map((item, idx) => (
                <tr key={idx} className="hover:bg-slate-50/80 transition-colors">
                  <td className="p-3.5">
                    {item.covered ? (
                      <span className="inline-flex items-center gap-1.5 text-xs font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-200">
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                        Covered
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-1.5 text-xs font-bold text-rose-700 bg-rose-50 px-2 py-0.5 rounded-full border border-rose-200">
                        <XCircle className="w-3.5 h-3.5 text-rose-600" />
                        Uncovered
                      </span>
                    )}
                  </td>
                  <td className="p-3.5 font-bold text-slate-900">
                    {item.requirement}
                  </td>
                  <td className="p-3.5 font-mono text-teal-700 font-bold text-xs">
                    {item.evidence || '—'}
                  </td>
                  <td className="p-3.5 text-slate-600 leading-relaxed text-xs">
                    {item.detail}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Conflict / Gap Action Navigation */}
      <div className="bg-amber-50 border border-amber-200 rounded-xl p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <AlertCircle className="w-5 h-5 text-amber-600 shrink-0" />
          <div className="text-xs text-amber-900">
            <span className="font-bold">Coverage status:</span> {coveredCount === totalCount ? 'All visible requirements are supported by evidence from the active corpus.' : 'Some requirements may need human review before procurement issuance.'}
          </div>
        </div>
        <button
          onClick={() => onNavigateTab('conflicts-gaps')}
          className="px-3.5 py-1.5 bg-amber-600 hover:bg-amber-700 text-white rounded-lg text-xs font-bold shadow-sm transition-all flex items-center gap-1 shrink-0"
        >
          <span>Inspect Conflicts & Gaps</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </button>
      </div>

    </div>
  );
}
