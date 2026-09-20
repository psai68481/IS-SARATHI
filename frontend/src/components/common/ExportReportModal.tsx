import React from 'react';
import { X, Download, ShieldCheck, CheckCircle2, AlertTriangle, FileText } from 'lucide-react';
import { DashboardData } from '@/types';

interface ExportReportModalProps {
  isOpen: boolean;
  onClose: () => void;
  data: DashboardData;
}

export default function ExportReportModal({ isOpen, onClose, data }: ExportReportModalProps) {
  if (!isOpen) return null;

  const topRec = data.recommendations[0];
  const currentDate = new Date().toLocaleDateString('en-IN', {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  });

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="fixed inset-0 bg-black/60 z-50 flex items-center justify-center p-4 backdrop-blur-sm">
      <div className="bg-white rounded-2xl max-w-3xl w-full max-h-[90vh] flex flex-col shadow-2xl border border-slate-200 overflow-hidden animate-in fade-in zoom-in-95 duration-150">
        
        {/* Modal Header */}
        <div className="bg-[#1E2761] text-white px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-teal-300" />
            <h3 className="font-bold text-base">Procurement Standard Alignment Dossier</h3>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-lg hover:bg-white/10 text-slate-300 hover:text-white transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Body / Report Preview */}
        <div className="p-6 overflow-y-auto space-y-6 text-slate-800 text-xs sm:text-sm print:p-0">
          
          {/* Official Letterhead */}
          <div className="border-b-2 border-slate-900 pb-4 flex items-start justify-between">
            <div>
              <div className="text-xs font-black tracking-wider uppercase text-slate-500">
                Government e-Marketplace (GeM) &bull; Technical Review Division
              </div>
              <h1 className="text-lg font-black text-slate-900 mt-0.5">
                IS-SARATHI STANDARDS ALIGNMENT CERTIFICATE
              </h1>
              <p className="text-xs text-slate-600">
                Decision-Support Evidence Pack for Tender Verification & Mandatory QCO Compliance
              </p>
            </div>
            <div className="text-right text-xs">
              <div className="font-bold text-slate-800">Date: {currentDate}</div>
              <div className="text-slate-500">Report Ref: SARATHI-{Math.floor(100000 + Math.random() * 900000)}</div>
            </div>
          </div>

          {/* Tender Specification Summary */}
          <div className="bg-slate-50 p-4 rounded-xl border border-slate-200">
            <h4 className="font-bold text-slate-900 text-xs uppercase tracking-wide mb-1">
              Procurement Tender Specification
            </h4>
            <p className="text-xs text-slate-700 leading-relaxed italic">
              "{data.tenderQuery}"
            </p>
          </div>

          {/* Primary Recommended Standard */}
          {topRec && (
            <div className="border border-teal-200 bg-teal-50/50 p-4 rounded-xl">
              <div className="flex items-center justify-between mb-2">
                <span className="text-[11px] font-bold text-teal-800 bg-teal-100 px-2 py-0.5 rounded border border-teal-200 uppercase">
                  Primary Mandated Standard
                </span>
                <span className="font-extrabold text-teal-900 text-xs">
                  Match Confidence: {topRec.confidence}%
                </span>
              </div>
              <h3 className="font-black text-slate-900 text-base">
                {topRec.isNumber}: {topRec.title}
              </h3>
              <p className="text-xs text-slate-600 mt-1 leading-relaxed">
                {topRec.description}
              </p>

              <div className="mt-3 grid grid-cols-2 sm:grid-cols-3 gap-2 pt-3 border-t border-teal-200/60 text-xs">
                <div>
                  <span className="text-slate-500 block">Version / Reaffirmation:</span>
                  <strong className="text-slate-800">{topRec.latestVersion}</strong>
                </div>
                <div>
                  <span className="text-slate-500 block">BIS Certification:</span>
                  <strong className="text-amber-800">{topRec.certification.scheme} ({topRec.certification.status})</strong>
                </div>
                <div>
                  <span className="text-slate-500 block">Amendment Status:</span>
                  <strong className="text-slate-800">{topRec.amendment}</strong>
                </div>
              </div>
            </div>
          )}

          {/* Clause Verification Table */}
          <div>
            <h4 className="font-bold text-slate-900 text-xs uppercase tracking-wide mb-2 flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              Verified Requirements & Standard Clause Mapping
            </h4>
            <div className="border border-slate-200 rounded-lg overflow-hidden">
              <table className="w-full text-left text-xs border-collapse">
                <thead className="bg-slate-100 text-slate-600 font-bold border-b border-slate-200">
                  <tr>
                    <th className="p-2.5">Tender Parameter</th>
                    <th className="p-2.5">Standard Evidence</th>
                    <th className="p-2.5">Compliance Finding</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {topRec?.coverageMap.map((cov, idx) => (
                    <tr key={idx} className="hover:bg-slate-50">
                      <td className="p-2.5 font-semibold text-slate-800">{cov.requirement}</td>
                      <td className="p-2.5 text-teal-700 font-mono text-[11px]">{cov.evidence || 'N/A'}</td>
                      <td className="p-2.5 text-slate-600">{cov.detail}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Compliance & Conflict Advisory */}
          {data.conflicts.length > 0 && (
            <div className="bg-amber-50 border border-amber-200 p-4 rounded-xl text-xs text-amber-900">
              <div className="flex items-center gap-2 font-bold mb-1">
                <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0" />
                <span>Procurement Technical Flag / Conflict Warning</span>
              </div>
              <p className="leading-relaxed">
                {data.conflicts[0].tenderSpec} vs {data.conflicts[0].standardSpec}. {data.conflicts[0].impact}
              </p>
            </div>
          )}

          {/* Legal Sign-Off Disclaimer */}
          <div className="text-[11px] text-slate-500 border-t border-slate-200 pt-3 leading-relaxed">
            <strong>Legal Governance Note:</strong> IS-SARATHI is an AI-powered procurement decision-support engine. This report compiles evidence-grounded recommendations based on Bureau of Indian Standards (BIS) publications. Final standard citation and contract terms must be approved by the designated competent procurement officer.
          </div>

        </div>

        {/* Modal Footer */}
        <div className="bg-slate-50 border-t border-slate-200 px-6 py-3 flex items-center justify-between">
          <span className="text-xs text-slate-500">
            Export Format: Print / PDF Dossier
          </span>
          <div className="flex items-center gap-2">
            <button
              onClick={onClose}
              className="px-4 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-200 rounded-lg transition-colors"
            >
              Close
            </button>
            <button
              onClick={handlePrint}
              className="px-4 py-2 text-xs font-bold bg-[#028090] hover:bg-[#006d7b] text-white rounded-lg shadow-sm flex items-center gap-1.5 transition-all"
            >
              <Download className="w-4 h-4" />
              <span>Print / Download PDF</span>
            </button>
          </div>
        </div>

      </div>
    </div>
  );
}
