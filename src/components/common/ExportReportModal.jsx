import React from 'react';
import { 
  X, 
  Printer, 
  Award,
  AlertTriangle
} from 'lucide-react';
import ConfidenceBadge from './ConfidenceBadge';

export default function ExportReportModal({ isOpen, onClose, data }) {
  if (!isOpen) return null;

  const recommendations = data.recommendations || [];
  const topRec = recommendations[0];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
      <div className="bg-white rounded-2xl max-w-3xl w-full max-h-[90vh] flex flex-col shadow-2xl border border-slate-200 overflow-hidden animate-in fade-in zoom-in-95 duration-150">
        
        {/* Modal Top Header */}
        <div className="px-6 py-4 bg-slate-900 text-white flex items-center justify-between border-b border-slate-800">
          <div className="flex items-center gap-2">
            <Award className="w-5 h-5 text-teal-400" />
            <div>
              <h3 className="text-sm font-bold">
                IS-SARATHI Internal Decision-Support Report
              </h3>
              <p className="text-[11px] text-slate-400">
                Technical Standard Alignment & Decision Support for Procurement File
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Printable Report Body */}
        <div className="p-6 overflow-y-auto space-y-6 text-slate-800 text-xs leading-relaxed font-sans">
          
          {/* Header Banner */}
          <div className="border-b-2 border-slate-900 pb-4 flex items-center justify-between flex-wrap gap-2">
            <div>
              <div className="text-sm sm:text-base font-black text-slate-900 font-sans tracking-tight">
                IS-SARATHI INTERNAL DECISION-SUPPORT REPORT
              </div>
              <div className="text-[11px] text-slate-500 font-medium mt-0.5">
                Automated Technical Standard Alignment & Clause Verification Audit
              </div>
            </div>
            <div className="text-right">
              <div className="text-[10px] font-mono font-bold text-slate-500">REF: IS-SARATHI-DECISION-{Date.now().toString().slice(-6)}</div>
              <div className="text-[10px] text-slate-400">Date: {new Date().toLocaleDateString('en-IN')}</div>
            </div>
          </div>

          {/* Tender Query Scope */}
          <div className="bg-slate-50 p-3.5 rounded-lg border border-slate-200">
            <span className="font-bold uppercase text-[10px] text-slate-500 block mb-1">
              Procurement Tender Scope:
            </span>
            <p className="text-slate-800 font-medium italic">
              "{data.tenderQuery}"
            </p>
          </div>

          {/* Recommended Standard Primary Block OR Abstention Card */}
          {topRec ? (
            <div className="p-4 rounded-xl border-2 border-teal-600 bg-teal-50/40">
              <div className="flex items-center justify-between mb-2">
                <span className="text-[10px] font-extrabold uppercase tracking-wider text-teal-800 bg-teal-100 px-2 py-0.5 rounded">
                  Recommended Primary Standard
                </span>
                <ConfidenceBadge score={topRec.confidence} size="sm" />
              </div>

              <div className="text-lg font-black text-slate-900 font-sans">
                {topRec.isNumber}: {topRec.title}
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 mt-3 text-[11px] pt-2 border-t border-teal-200">
                <div>
                  <span className="text-slate-500 block">Status:</span>
                  <span className="font-bold text-emerald-700">{topRec.status}</span>
                </div>
                <div>
                  <span className="text-slate-500 block">Certification Scheme:</span>
                  <span className="font-bold text-amber-800">{topRec.certification?.scheme} ({topRec.certification?.status})</span>
                </div>
                <div>
                  <span className="text-slate-500 block">Reaffirmed Version:</span>
                  <span className="font-bold text-slate-800">{topRec.latestVersion}</span>
                </div>
              </div>
            </div>
          ) : (
            <div className="p-4 rounded-xl border-2 border-amber-500 bg-amber-50/60 text-amber-900 space-y-2">
              <div className="flex items-center gap-2 font-bold text-sm text-amber-950">
                <AlertTriangle className="w-5 h-5 text-amber-600" />
                <span>INSUFFICIENT EVIDENCE — Standard Verification Required</span>
              </div>
              <p className="text-xs leading-relaxed">
                {data.abstentionReason || "No verified applicable Indian Standard was found in the current IS-SARATHI knowledge base."}
              </p>
            </div>
          )}

          {/* Verification Clauses */}
          {topRec && topRec.coverageMap && topRec.coverageMap.length > 0 && (
            <div>
              <span className="font-bold uppercase text-[10px] text-slate-600 block mb-2">
                Clause-by-Clause Verification Evidence:
              </span>
              <div className="overflow-x-auto">
                <table className="w-full border border-slate-200 text-left text-xs">
                  <thead className="bg-slate-100 border-b border-slate-200 font-bold text-slate-700">
                    <tr>
                      <th className="p-2">Requirement</th>
                      <th className="p-2">Evidence Clause</th>
                      <th className="p-2 text-center">Status</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {topRec.coverageMap.map((c, i) => (
                      <tr key={i}>
                        <td className="p-2 font-medium">{c.requirement}</td>
                        <td className="p-2 font-mono font-bold text-teal-700">{c.evidence || "Contractual"}</td>
                        <td className="p-2 text-center">
                          <span className={`font-bold ${c.covered ? "text-emerald-700" : "text-amber-700"}`}>
                            {c.covered ? "✓ Covered" : "⚠ Action Req."}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

        </div>

        {/* Footer Actions */}
        <div className="px-6 py-3.5 bg-slate-50 border-t border-slate-200 flex flex-wrap items-center justify-between gap-2">
          <span className="text-[11px] text-slate-500 italic">
            Generated by IS-SARATHI Internal Decision-Support Engine
          </span>
          <div className="flex items-center gap-2">
            <button
              onClick={() => window.print()}
              className="px-4 py-2 bg-slate-900 hover:bg-slate-800 text-white rounded-lg text-xs font-bold flex items-center gap-1.5 shadow-sm"
            >
              <Printer className="w-4 h-4" />
              <span>Print Report</span>
            </button>
            <button
              onClick={onClose}
              className="px-4 py-2 bg-slate-200 hover:bg-slate-300 text-slate-800 rounded-lg text-xs font-semibold"
            >
              Close
            </button>
          </div>
        </div>

      </div>
    </div>
  );
}

