import React from 'react';
import { 
  CheckSquare, 
  CheckCircle2, 
  AlertTriangle, 
  FileCheck, 
  Info, 
  ArrowRight 
} from 'lucide-react';

export default function RequirementCoverageTab({ data, onNavigateTab }) {
  const topRec = data.recommendations[0];
  const coverageMap = topRec.coverageMap || [];
  
  const coveredCount = coverageMap.filter(c => c.covered).length;
  const totalCount = coverageMap.length;
  const coveragePercent = Math.round((coveredCount / totalCount) * 100);

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-200 pb-4">
        <div>
          <h2 className="text-xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
            <CheckSquare className="w-5 h-5 text-teal-600" />
            Requirement Coverage & Clause Evidence Matrix
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Audit trail mapping tender requirements to specific Indian Standard clauses and compliance verification evidence.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold px-2.5 py-1 bg-emerald-50 text-emerald-800 border border-emerald-200 rounded-md">
            {coveredCount} of {totalCount} Covered ({coveragePercent}%)
          </span>
        </div>
      </div>

      {/* Coverage Progress Summary Card */}
      <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="text-xs font-bold uppercase tracking-wider text-slate-500">
              Evaluated Standard
            </div>
            <div className="text-base font-extrabold text-slate-900 mt-0.5">
              {topRec.isNumber}: {topRec.title}
            </div>
          </div>

          {/* Progress bar */}
          <div className="sm:w-72">
            <div className="flex justify-between text-xs font-bold mb-1.5">
              <span className="text-slate-600">Clause Compliance Score</span>
              <span className={coveragePercent >= 80 ? "text-emerald-600" : "text-amber-600"}>
                {coveragePercent}%
              </span>
            </div>
            <div className="w-full h-2.5 bg-slate-100 rounded-full overflow-hidden border border-slate-200">
              <div 
                className={`h-full rounded-full transition-all duration-500 ${
                  coveragePercent >= 80 ? "bg-emerald-500" : "bg-amber-500"
                }`}
                style={{ width: `${coveragePercent}%` }}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Coverage Table */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="p-4 bg-slate-50 border-b border-slate-200 flex flex-wrap items-center justify-between gap-2">
          <div className="text-xs font-bold uppercase tracking-wider text-slate-700 flex items-center gap-2">
            <FileCheck className="w-4 h-4 text-teal-600" />
            Clause-by-Clause Verification Table
          </div>
          <span className="text-[11px] text-slate-500">
            Source: Bureau of Indian Standards Official Specification
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-100/70 border-b border-slate-200 text-[11px] font-bold text-slate-600 uppercase tracking-wider">
                <th className="py-3 px-4 min-w-[150px]">Requirement</th>
                <th className="py-3 px-4 min-w-[120px]">Evidence Clause</th>
                <th className="py-3 px-4 min-w-[240px]">Technical Specification & Clause Detail</th>
                <th className="py-3 px-4 min-w-[100px] text-center">Covered</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-xs text-slate-800">
              {coverageMap.map((item, idx) => (
                <tr key={idx} className="hover:bg-slate-50/80 transition-colors">
                  
                  {/* Requirement Name */}
                  <td className="py-3.5 px-4 font-bold text-slate-900">
                    <div className="flex items-center gap-2">
                      <span className="w-1.5 h-1.5 rounded-full bg-slate-400" />
                      {item.requirement}
                    </div>
                  </td>

                  {/* Evidence Clause */}
                  <td className="py-3.5 px-4 font-mono font-bold">
                    {item.evidence ? (
                      <span className="inline-flex items-center px-2 py-0.5 rounded bg-teal-50 text-teal-800 border border-teal-200 text-xs">
                        {item.evidence}
                      </span>
                    ) : (
                      <span className="text-slate-400 italic text-xs">
                        None (Out of scope)
                      </span>
                    )}
                  </td>

                  {/* Clause Detail */}
                  <td className="py-3.5 px-4 text-slate-600 leading-relaxed">
                    {item.detail}
                  </td>

                  {/* Covered Status Icon */}
                  <td className="py-3.5 px-4 text-center">
                    {item.covered ? (
                      <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-50 text-emerald-700 border border-emerald-200 shadow-sm">
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                        Covered
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-bold bg-amber-50 text-amber-700 border border-amber-200 shadow-sm">
                        <AlertTriangle className="w-3.5 h-3.5 text-amber-600" />
                        Uncovered
                      </span>
                    )}
                  </td>

                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Table Footer / Gap Notice */}
        <div className="p-4 bg-slate-50 border-t border-slate-200 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs">
          <div className="flex items-center gap-2 text-slate-600">
            <Info className="w-4 h-4 text-amber-600 shrink-0" />
            <span>
              1 item requires procurement clause customization: <strong>Installation Requirement</strong> is a contractual scope item.
            </span>
          </div>

          <button
            onClick={() => onNavigateTab('conflicts-gaps')}
            className="text-xs font-bold text-teal-700 hover:text-teal-900 flex items-center gap-1"
          >
            <span>Review Gaps & Conflicts</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

    </div>
  );
}
