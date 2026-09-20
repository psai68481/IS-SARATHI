import React from 'react';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer, 
  Cell
} from 'recharts';
import { 
  FileCheck, 
  Percent, 
  BookOpen, 
  Clock, 
  ArrowUpRight, 
  Sparkles, 
  AlertTriangle,
  Award,
  ChevronRight
} from 'lucide-react';
import ConfidenceBadge from '../common/ConfidenceBadge';

export default function DashboardTab({ data, onNavigateTab }) {
  const stats = data.stats;
  const distribution = data.confidenceDistribution;
  const topRec = data.recommendations[0];

  return (
    <div className="space-y-6">
      
      {/* Top Banner / Welcome */}
      <div className="bg-gradient-to-r from-[#1E2761] via-[#162054] to-[#028090] rounded-2xl p-5 sm:p-6 text-white shadow-md relative overflow-hidden">
        <div className="absolute right-0 top-0 bottom-0 opacity-10 pointer-events-none hidden sm:flex items-center pr-6">
          <Award className="w-56 h-56 text-white -mr-10" />
        </div>
        <div className="relative z-10 max-w-2xl">
          <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-white/15 backdrop-blur-sm text-xs font-semibold text-teal-200 mb-3 border border-white/20">
            <Sparkles className="w-3.5 h-3.5" />
            AI Recommendation Engine Active
          </div>
          <h1 className="text-xl sm:text-2xl font-black tracking-tight text-white mb-2">
            Indian Standards Procurement Assistant
          </h1>
          <p className="text-slate-200 text-xs sm:text-sm leading-relaxed mb-4">
            IS-SARATHI reads tender specifications, extracts required parameters, cross-maps Indian Standards (IS/ISO/IEC), detects non-compliance conflicts, and flags mandatory BIS Quality Control Orders (QCO).
          </p>
          <div className="flex flex-wrap items-center gap-3">
            <button
              onClick={() => onNavigateTab('tender-analysis')}
              className="px-4 py-2 rounded-lg bg-teal-500 hover:bg-teal-600 text-white text-xs font-bold shadow-sm transition-all duration-150 flex items-center gap-1.5 active:scale-95"
            >
              <span>Analyze Current Tender</span>
              <ArrowUpRight className="w-4 h-4" />
            </button>
            <button
              onClick={() => onNavigateTab('recommendations')}
              className="px-4 py-2 rounded-lg bg-white/10 hover:bg-white/20 text-white text-xs font-bold backdrop-blur-sm transition-all duration-150 border border-white/20 flex items-center gap-1.5"
            >
              <span>View Recommendations {topRec ? `(${topRec.isNumber})` : ""}</span>
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* 4 Stat Overview Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        
        {/* Card 1: Total Tenders */}
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm hover:border-slate-300 transition-all">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">
              Total Tenders Analyzed
            </span>
            <div className="w-8 h-8 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center">
              <FileCheck className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-3xl font-extrabold text-slate-900 font-sans">
              {stats.totalTendersAnalyzed}
            </span>
            <span className="text-xs font-semibold text-emerald-600 flex items-center">
              +12% this month
            </span>
          </div>
          <div className="mt-2 text-xs text-slate-500">
            Automated clause matching applied
          </div>
        </div>

        {/* Card 2: Avg Confidence */}
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm hover:border-slate-300 transition-all">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">
              Avg AI Confidence
            </span>
            <div className="w-8 h-8 rounded-lg bg-emerald-50 text-emerald-600 flex items-center justify-center">
              <Percent className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-3xl font-extrabold text-slate-900 font-sans">
              {stats.avgConfidence}%
            </span>
            <span className="text-xs font-semibold text-emerald-600">
              High Precision
            </span>
          </div>
          <div className="mt-2 text-xs text-slate-500">
            Across 4,200+ requirement clauses
          </div>
        </div>

        {/* Card 3: Standards in KB */}
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm hover:border-slate-300 transition-all">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">
              Standards in KB
            </span>
            <div className="w-8 h-8 rounded-lg bg-teal-50 text-teal-600 flex items-center justify-center">
              <BookOpen className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-3xl font-extrabold text-slate-900 font-sans">
              {stats.standardsInKB}
            </span>
            <span className="text-xs font-semibold text-teal-600">
              BIS Direct
            </span>
          </div>
          <div className="mt-2 text-xs text-slate-500">
            Includes test methods & materials
          </div>
        </div>

        {/* Card 4: Pending Reviews */}
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm hover:border-slate-300 transition-all">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">
              Pending Reviews
            </span>
            <div className="w-8 h-8 rounded-lg bg-amber-50 text-amber-600 flex items-center justify-center">
              <Clock className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-3xl font-extrabold text-slate-900 font-sans">
              {stats.pendingReviews}
            </span>
            <span className="text-xs font-semibold text-amber-600 flex items-center gap-1">
              <AlertTriangle className="w-3 h-3" />
              Human verification
            </span>
          </div>
          <div className="mt-2 text-xs text-slate-500">
            Flags requiring procurement officer sign-off
          </div>
        </div>

      </div>

      {/* Main Charts & Quick Action Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Recharts Bar Chart: Confidence Distribution */}
        <div className="lg:col-span-2 bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-4">
            <div>
              <h3 className="font-bold text-slate-900 text-sm">
                Confidence Distribution Across Recent Recommendations
              </h3>
              <p className="text-xs text-slate-500">
                Categorization of AI matching confidence scores across all evaluated specifications
              </p>
            </div>
            <div className="flex flex-wrap items-center gap-2 text-xs text-slate-500 font-medium">
              <span className="inline-flex items-center gap-1"><span className="w-2.5 h-2.5 rounded-full bg-emerald-500"></span> 90%+</span>
              <span className="inline-flex items-center gap-1"><span className="w-2.5 h-2.5 rounded-full bg-teal-500"></span> 80-89%</span>
              <span className="inline-flex items-center gap-1"><span className="w-2.5 h-2.5 rounded-full bg-amber-500"></span> 70-79%</span>
              <span className="inline-flex items-center gap-1"><span className="w-2.5 h-2.5 rounded-full bg-rose-500"></span> &lt;70%</span>
            </div>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={distribution} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E2E8F0" />
                <XAxis 
                  dataKey="range" 
                  tick={{ fill: '#64748B', fontSize: 11, fontWeight: 500 }}
                  axisLine={{ stroke: '#CBD5E1' }}
                />
                <YAxis 
                  tick={{ fill: '#64748B', fontSize: 11 }}
                  axisLine={{ stroke: '#CBD5E1' }}
                />
                <Tooltip
                  cursor={{ fill: '#F8FAFC' }}
                  content={({ active, payload }) => {
                    if (active && payload && payload.length) {
                      const item = payload[0].payload;
                      return (
                        <div className="bg-slate-900 text-white text-xs p-2.5 rounded-lg shadow-lg">
                          <p className="font-bold">{item.range}</p>
                          <p className="text-teal-300 mt-1">Tenders count: <strong>{item.count}</strong></p>
                        </div>
                      );
                    }
                    return null;
                  }}
                />
                <Bar dataKey="count" radius={[6, 6, 0, 0]}>
                  {distribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.fill} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div className="mt-3 pt-3 border-t border-slate-100 flex flex-wrap items-center justify-between gap-2 text-xs text-slate-500">
            <span>High-accuracy tier (&ge;80%): <strong>38 / 47 (80.8%)</strong></span>
            <span className="text-teal-600 font-semibold cursor-pointer hover:underline" onClick={() => onNavigateTab('recommendations')}>
              Review AI Model Calibration &rarr;
            </span>
          </div>
        </div>

        {/* Right Column: Active Tender Spotlight & Knowledge Base Status */}
        <div className="space-y-4">
          
          {/* Active Tender Quick Card */}
          <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
            <div className="flex items-center justify-between mb-3">
              <span className="text-[11px] font-bold text-teal-700 bg-teal-50 px-2 py-0.5 rounded border border-teal-200 uppercase">
                Active Analysis Case
              </span>
              <ConfidenceBadge score={topRec.confidence} size="sm" />
            </div>
            <h4 className="font-bold text-slate-900 text-sm leading-snug">
              {topRec.isNumber}: {topRec.title}
            </h4>
            <p className="text-xs text-slate-500 mt-1 line-clamp-2">
              {data.tenderQuery}
            </p>
            
            <div className="mt-4 pt-3 border-t border-slate-100 space-y-2">
              <div className="flex justify-between text-xs">
                <span className="text-slate-500">Certification:</span>
                <span className="font-bold text-amber-700">{topRec.certification.scheme} ({topRec.certification.status})</span>
              </div>
              <div className="flex justify-between text-xs">
                <span className="text-slate-500">Reaffirmation:</span>
                <span className="font-medium text-slate-700">{topRec.latestVersion}</span>
              </div>
            </div>

            <button
              onClick={() => onNavigateTab('recommendations')}
              className="w-full mt-4 py-2 bg-slate-900 hover:bg-slate-800 text-white rounded-lg text-xs font-semibold transition-all flex items-center justify-center gap-1"
            >
              <span>Explore Full Recommendation</span>
              <ChevronRight className="w-3.5 h-3.5" />
            </button>
          </div>

          {/* Domain Breakdown mini-card */}
          <div className="bg-slate-50 p-4 rounded-xl border border-slate-200">
            <div className="text-xs font-bold text-slate-700 uppercase tracking-wide mb-2 flex items-center justify-between">
              <span>Domain Index Coverage</span>
              <span className="text-[10px] text-slate-500">{stats.standardsInKB || 28} Standards</span>
            </div>
            <div className="space-y-2">
              {data.domainBreakdown.slice(0, 3).map((d, i) => (
                <div key={i} className="text-xs">
                  <div className="flex justify-between text-slate-600 mb-0.5">
                    <span className="truncate pr-2">{d.domain}</span>
                    <span className="font-semibold text-slate-800">{d.share}</span>
                  </div>
                  <div className="w-full h-1.5 bg-slate-200 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-teal-500 rounded-full"
                      style={{ width: d.share }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

        </div>

      </div>

    </div>
  );
}
