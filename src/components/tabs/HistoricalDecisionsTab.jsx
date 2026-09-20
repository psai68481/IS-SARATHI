import React, { useState } from 'react';
import { 
  History, 
  Search, 
  Filter, 
  ArrowRight
} from 'lucide-react';

export default function HistoricalDecisionsTab({ data, onNavigateTab }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('ALL');

  const history = data.historicalDecisions || [];

  const filteredHistory = history.filter(item => {
    const matchesSearch = 
      item.caseId.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.aiRecommendation.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.humanDecision.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.reason.toLowerCase().includes(searchTerm.toLowerCase());

    const matchesStatus = statusFilter === 'ALL' || item.validationStatus.toUpperCase() === statusFilter;

    return matchesSearch && matchesStatus;
  });

  const getStatusDot = (status) => {
    switch (status) {
      case "Validated":
        return (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">
            <span className="w-2 h-2 rounded-full bg-emerald-500" />
            Validated
          </span>
        );
      case "Unverified":
        return (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-bold bg-amber-50 text-amber-700 border border-amber-200">
            <span className="w-2 h-2 rounded-full bg-amber-500 animate-pulse" />
            Unverified
          </span>
        );
      case "Rejected":
        return (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-bold bg-rose-50 text-rose-700 border border-rose-200">
            <span className="w-2 h-2 rounded-full bg-rose-500" />
            Rejected
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-slate-100 text-slate-700">
            <span className="w-2 h-2 rounded-full bg-slate-400" />
            {status}
          </span>
        );
    }
  };

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-200 pb-4">
        <div>
          <h2 className="text-xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
            <History className="w-5 h-5 text-teal-600" />
            Historical Procurement Audit & Decisions Log
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Immutable log of previous tender classifications, procurement officer overrides, and technical justification rationales.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold px-2.5 py-1 bg-slate-100 text-slate-700 rounded-md border border-slate-200">
            {history.length} Cases Logged
          </span>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-sm flex flex-col sm:flex-row items-center justify-between gap-4">
        {/* Search input */}
        <div className="relative w-full sm:w-80">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search Case ID, Department, Standard..."
            className="w-full text-xs bg-slate-50 border border-slate-200 rounded-lg pl-9 pr-3 py-2 text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-1 focus:ring-teal-500 focus:bg-white"
          />
        </div>

        {/* Filter buttons */}
        <div className="flex items-center gap-1.5 self-start sm:self-auto flex-wrap">
          <span className="text-xs font-semibold text-slate-500 mr-1 flex items-center gap-1">
            <Filter className="w-3.5 h-3.5 text-slate-400" />
            Status:
          </span>
          {['ALL', 'VALIDATED', 'UNVERIFIED', 'REJECTED'].map((st) => (
            <button
              key={st}
              onClick={() => setStatusFilter(st)}
              className={`px-2.5 py-1 rounded-md text-xs font-semibold transition-all ${
                statusFilter === st
                  ? "bg-slate-900 text-white shadow-sm"
                  : "bg-slate-100 text-slate-600 hover:bg-slate-200"
              }`}
            >
              {st}
            </button>
          ))}
        </div>
      </div>

      {/* History Table */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-100/80 border-b border-slate-200 text-[11px] font-bold text-slate-600 uppercase tracking-wider">
                <th className="py-3 px-4 min-w-[120px]">Case ID</th>
                <th className="py-3 px-4 min-w-[160px]">Tender Title & Dept</th>
                <th className="py-3 px-4 min-w-[160px]">AI Recommendation</th>
                <th className="py-3 px-4 min-w-[160px]">Human Decision</th>
                <th className="py-3 px-4 min-w-[220px]">Justification & Reason</th>
                <th className="py-3 px-4 min-w-[120px] text-center">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-xs text-slate-800">
              {filteredHistory.map((item, idx) => {
                const isOverridden = item.aiRecommendation !== item.humanDecision;

                return (
                  <tr key={idx} className="hover:bg-slate-50/80 transition-colors">
                    
                    {/* Case ID */}
                    <td className="py-3.5 px-4 font-mono font-bold text-teal-700">
                      <div>{item.caseId}</div>
                      <div className="text-[10px] text-slate-400 font-sans font-normal">{item.date}</div>
                    </td>

                    {/* Title & Dept */}
                    <td className="py-3.5 px-4">
                      <div className="font-bold text-slate-900">{item.title}</div>
                      <div className="text-[11px] text-slate-500 mt-0.5">{item.department}</div>
                    </td>

                    {/* AI Recommendation */}
                    <td className="py-3.5 px-4">
                      <span className="font-bold text-slate-800 bg-slate-100 px-2 py-0.5 rounded border border-slate-200 inline-block">
                        {item.aiRecommendation}
                      </span>
                    </td>

                    {/* Human Decision */}
                    <td className="py-3.5 px-4">
                      <div className="flex items-center gap-1.5 flex-wrap">
                        <span className={`font-bold px-2 py-0.5 rounded border inline-block ${
                          isOverridden
                            ? "bg-purple-50 text-purple-800 border-purple-200"
                            : "bg-emerald-50 text-emerald-800 border-emerald-200"
                        }`}>
                          {item.humanDecision}
                        </span>
                        {isOverridden && (
                          <span className="text-[10px] font-bold text-purple-600 uppercase" title="Human Override Applied">
                            Override
                          </span>
                        )}
                      </div>
                    </td>

                    {/* Reason */}
                    <td className="py-3.5 px-4 text-slate-600 leading-relaxed">
                      {item.reason}
                    </td>

                    {/* Status */}
                    <td className="py-3.5 px-4 text-center">
                      {getStatusDot(item.validationStatus)}
                    </td>

                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>

        {/* Footer */}
        <div className="p-4 bg-slate-50 border-t border-slate-200 flex flex-col sm:flex-row items-center justify-between gap-2 text-xs text-slate-500">
          <span>Showing {filteredHistory.length} of {history.length} decision records</span>
          <button 
            onClick={() => onNavigateTab('learning')}
            className="text-xs font-bold text-teal-700 hover:text-teal-900 flex items-center gap-1"
          >
            <span>Examine AI Override Feedback Loop</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

    </div>
  );
}
