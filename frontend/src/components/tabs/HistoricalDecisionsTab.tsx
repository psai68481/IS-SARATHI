import React, { useState } from 'react';
import { 
  History, 
  Search, 
  Filter, 
  CheckCircle2, 
  Clock, 
  AlertCircle,
  Building2,
  Calendar
} from 'lucide-react';
import { DashboardData, HistoricalDecision } from '@/types';

interface HistoricalDecisionsTabProps {
  data: DashboardData;
  onNavigateTab: (tabId: string) => void;
}

export default function HistoricalDecisionsTab({ data, onNavigateTab }: HistoricalDecisionsTabProps) {
  const [searchTerm, setSearchTerm] = useState('');
  const decisions = data.historicalDecisions || [];

  const filtered = decisions.filter(d => 
    d.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    d.caseId.toLowerCase().includes(searchTerm.toLowerCase()) ||
    d.department.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'Validated':
        return (
          <span className="inline-flex items-center gap-1 text-[11px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
            <CheckCircle2 className="w-3 h-3 text-emerald-600" />
            Validated
          </span>
        );
      case 'Unverified':
        return (
          <span className="inline-flex items-center gap-1 text-[11px] font-bold text-amber-700 bg-amber-50 px-2 py-0.5 rounded border border-amber-200">
            <Clock className="w-3 h-3 text-amber-600" />
            Pending Review
          </span>
        );
      case 'Rejected':
        return (
          <span className="inline-flex items-center gap-1 text-[11px] font-bold text-rose-700 bg-rose-50 px-2 py-0.5 rounded border border-rose-200">
            <AlertCircle className="w-3 h-3 text-rose-600" />
            Rejected
          </span>
        );
      default:
        return null;
    }
  };

  return (
    <div className="space-y-6">
      
      {/* Header Info */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-200 pb-4">
        <div>
          <h2 className="text-xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
            <History className="w-5 h-5 text-teal-600" />
            Historical Procurement Decisions & Case Library
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Audit trail of past procurement tender cases, AI recommendations, officer verifications, and justifiable overrides.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold px-2.5 py-1 bg-slate-100 text-slate-700 rounded-md border border-slate-200">
            5 Audited Case Records
          </span>
        </div>
      </div>

      {/* Search Bar */}
      <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex items-center gap-3">
        <Search className="w-4 h-4 text-slate-400 shrink-0" />
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder="Filter by case ID, tender title, or government department..."
          className="w-full text-xs sm:text-sm bg-transparent focus:outline-none text-slate-800 placeholder:text-slate-400"
        />
        {searchTerm && (
          <button onClick={() => setSearchTerm('')} className="text-xs text-slate-400 hover:text-slate-600">
            Clear
          </button>
        )}
      </div>

      {/* Decision Cards List */}
      <div className="space-y-3">
        {filtered.map((d, idx) => (
          <div 
            key={idx}
            className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm hover:border-slate-300 transition-all space-y-3"
          >
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div className="flex items-center gap-2">
                <span className="text-xs font-mono font-bold text-teal-700 bg-teal-50 px-2.5 py-0.5 rounded border border-teal-200">
                  {d.caseId}
                </span>
                <span className="text-xs text-slate-400 flex items-center gap-1">
                  <Calendar className="w-3.5 h-3.5" />
                  {d.date}
                </span>
                <span className="text-xs text-slate-600 flex items-center gap-1 font-medium">
                  <Building2 className="w-3.5 h-3.5 text-slate-400" />
                  {d.department}
                </span>
              </div>
              <div>
                {getStatusBadge(d.validationStatus)}
              </div>
            </div>

            <h3 className="text-sm sm:text-base font-bold text-slate-900">
              {d.title}
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-1">
              <div className="bg-slate-50 p-3 rounded-lg border border-slate-100">
                <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-0.5">
                  AI Recommendation
                </span>
                <span className="text-xs font-semibold text-slate-800">
                  {d.aiRecommendation}
                </span>
              </div>

              <div className="bg-slate-50 p-3 rounded-lg border border-slate-100">
                <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-0.5">
                  Human Officer Determination
                </span>
                <span className="text-xs font-bold text-teal-900">
                  {d.humanDecision}
                </span>
              </div>
            </div>

            <div className="text-xs text-slate-600 leading-relaxed bg-slate-50 p-3 rounded-lg border border-slate-100">
              <strong className="text-slate-800">Officer Justification: </strong>
              {d.reason}
            </div>
          </div>
        ))}
      </div>

    </div>
  );
}
