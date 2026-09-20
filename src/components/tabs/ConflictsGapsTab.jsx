import React from 'react';
import { 
  AlertTriangle, 
  ShieldAlert, 
  UserCheck, 
  FileWarning,
  Flame,
  AlertCircle,
  CheckCircle
} from 'lucide-react';

export default function ConflictsGapsTab({ data, onNavigateTab }) {
  const gaps = data.gaps || [];
  const conflicts = data.conflicts || [];

  return (
    <div className="space-y-8">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-200 pb-4">
        <div>
          <h2 className="text-xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-amber-500" />
            Specification Conflicts & Missing Gaps
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Automated discrepancy detection flagging tender terms that exceed Indian Standard safety limits or lack critical test specifications.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs font-bold px-2.5 py-1 bg-amber-50 text-amber-800 border border-amber-300 rounded-md">
            {gaps.length} Gaps
          </span>
          <span className="text-xs font-bold px-2.5 py-1 bg-rose-50 text-rose-800 border border-rose-300 rounded-md">
            {conflicts.length} Critical Conflicts
          </span>
        </div>
      </div>

      {/* SECTION 1: Specification Conflicts (Side-by-Side Comparison) */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-bold uppercase tracking-wider text-slate-700 flex items-center gap-2">
            <ShieldAlert className="w-4 h-4 text-rose-600" />
            Active Parameter Conflicts ({conflicts.length})
          </h3>
          <span className="text-xs text-slate-500">
            Requires technical amendment before tender publication
          </span>
        </div>

        <div className="space-y-4">
          {conflicts.map((item, idx) => (
            <div 
              key={idx}
              className="bg-white rounded-xl border border-rose-200 shadow-sm overflow-hidden"
            >
              {/* Conflict Header Bar */}
              <div className="bg-rose-50/70 px-4 sm:px-5 py-3 border-b border-rose-200 flex flex-wrap items-center justify-between gap-2">
                <div className="flex items-center gap-2 text-rose-900 font-bold text-xs">
                  <Flame className="w-4 h-4 text-rose-600 shrink-0" />
                  <span>Conflict Case #{idx + 1}: Specification Limit Mismatch</span>
                </div>
                
                {/* Red Severity Tag */}
                <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-rose-100 text-rose-800 border border-rose-300">
                  <UserCheck className="w-3.5 h-3.5 text-rose-600" />
                  {item.severity || "Human review recommended"}
                </span>
              </div>

              {/* Side-by-Side Comparison Grid */}
              <div className="p-4 sm:p-5 grid grid-cols-1 md:grid-cols-2 gap-4">
                
                {/* Tender Specification Box */}
                <div className="bg-slate-50 p-4 rounded-xl border border-slate-200">
                  <div className="text-[11px] font-bold uppercase tracking-wider text-slate-500 mb-1">
                    Tender Document Specification
                  </div>
                  <div className="text-sm font-bold text-slate-900">
                    {item.tenderSpec}
                  </div>
                  <div className="mt-2 text-xs text-rose-600 font-medium">
                    &bull; Exceeds standard operating envelope
                  </div>
                </div>

                {/* Indian Standard Specification Box */}
                <div className="bg-teal-50/50 p-4 rounded-xl border border-teal-200">
                  <div className="text-[11px] font-bold uppercase tracking-wider text-teal-800 mb-1">
                    IS 2925 Standard Baseline
                  </div>
                  <div className="text-sm font-bold text-teal-950">
                    {item.standardSpec}
                  </div>
                  <div className="mt-2 text-xs text-teal-700 font-medium">
                    &bull; Governed by BIS certified test envelope
                  </div>
                </div>

              </div>

              {/* Impact / Advisory Note */}
              {item.impact && (
                <div className="px-4 sm:px-5 py-3 bg-slate-50 border-t border-slate-200 text-xs text-slate-700 flex items-start gap-2">
                  <AlertCircle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
                  <div>
                    <strong className="text-slate-900">Procurement Officer Advisory: </strong>
                    {item.impact}
                  </div>
                </div>
              )}

            </div>
          ))}
        </div>
      </div>

      {/* SECTION 2: Gap Warnings (Amber Alert Boxes) */}
      <div className="space-y-4 pt-2">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-bold uppercase tracking-wider text-slate-700 flex items-center gap-2">
            <FileWarning className="w-4 h-4 text-amber-500" />
            Unspecified Parameters & Missing Quality Gaps ({gaps.length})
          </h3>
          <span className="text-xs text-slate-500">
            Recommended clauses to append in RFP/Tender Addendum
          </span>
        </div>

        <div className="space-y-3">
          {gaps.map((gapText, idx) => (
            <div 
              key={idx}
              className="bg-amber-50/80 border border-amber-300 rounded-xl p-4 flex items-start gap-3.5 shadow-sm"
            >
              <div className="w-7 h-7 rounded-lg bg-amber-200 text-amber-900 flex items-center justify-center shrink-0 mt-0.5">
                <AlertTriangle className="w-4 h-4" />
              </div>

              <div className="flex-1">
                <div className="flex items-center justify-between flex-wrap gap-1">
                  <span className="text-xs font-bold uppercase tracking-wider text-amber-900">
                    Quality Gap #{idx + 1}
                  </span>
                  <span className="text-[11px] font-semibold text-amber-800 bg-amber-100 px-2 py-0.5 rounded border border-amber-200">
                    Tender Omission
                  </span>
                </div>
                <p className="text-xs text-amber-950 font-medium mt-1 leading-relaxed">
                  {gapText}
                </p>
                <div className="mt-2 text-[11px] text-amber-800 flex items-center gap-1.5">
                  <CheckCircle className="w-3.5 h-3.5 text-amber-700 shrink-0" />
                  <span>Recommended Action: Incorporate mandatory IS 2925 (Part 2) drop test clause in Section 4.2.</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
}
