import React from 'react';
import { 
  GitFork, 
  FlaskConical, 
  ShieldAlert, 
  Component, 
  ArrowUpRight,
  Share2,
  BookOpen
} from 'lucide-react';
import { DashboardData } from '@/types';

interface RelatedStandardsTabProps {
  data: DashboardData;
}

export default function RelatedStandardsTab({ data }: RelatedStandardsTabProps) {
  const topRec = data.recommendations[0];
  const relatedList = topRec?.relatedStandards || [];

  const getRelationshipIcon = (type: string) => {
    switch (type) {
      case 'Test Method':
        return <FlaskConical className="w-4 h-4 text-purple-600" />;
      case 'Safety Standard':
        return <ShieldAlert className="w-4 h-4 text-emerald-600" />;
      case 'Material Standard':
        return <Component className="w-4 h-4 text-blue-600" />;
      default:
        return <BookOpen className="w-4 h-4 text-slate-600" />;
    }
  };

  const getBadgeStyle = (type: string) => {
    switch (type) {
      case 'Test Method':
        return 'bg-purple-50 text-purple-700 border-purple-200';
      case 'Safety Standard':
        return 'bg-emerald-50 text-emerald-700 border-emerald-200';
      case 'Material Standard':
        return 'bg-blue-50 text-blue-700 border-blue-200';
      default:
        return 'bg-slate-100 text-slate-700 border-slate-200';
    }
  };

  return (
    <div className="space-y-6">
      
      {/* Header Info */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-200 pb-4">
        <div>
          <h2 className="text-xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
            <GitFork className="w-5 h-5 text-teal-600" />
            Standards Relationship Graph & Allied References
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Multi-hop normative references, test methods, safety standards, and raw material specifications.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold px-2.5 py-1 bg-slate-100 text-slate-700 rounded-md border border-slate-200 flex items-center gap-1.5">
            <Share2 className="w-3.5 h-3.5 text-slate-500" />
            Dependency Graph Engine
          </span>
        </div>
      </div>

      {/* Primary Center Anchor Card */}
      <div className="bg-[#1E2761] text-white p-5 rounded-xl shadow-md">
        <div className="text-[11px] font-bold text-teal-300 uppercase tracking-wider mb-1">
          Root Reference Standard (Node 0)
        </div>
        <h3 className="text-lg font-black tracking-tight">
          {topRec?.isNumber}: {topRec?.title}
        </h3>
        <p className="text-xs text-slate-300 mt-1">
          Automated multi-hop graph expansion traverses direct normative citations, test specifications, and raw polymer testing protocols.
        </p>
      </div>

      {/* Relationship Graph Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {relatedList.map((rel, idx) => (
          <div 
            key={idx}
            className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm hover:border-teal-400 hover:shadow-md transition-all flex flex-col justify-between"
          >
            <div>
              <div className="flex items-center justify-between mb-3">
                <span className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-bold border ${getBadgeStyle(rel.type)}`}>
                  {getRelationshipIcon(rel.type)}
                  {rel.type}
                </span>
                <span className="text-[10px] font-bold text-slate-400">
                  Hop 1
                </span>
              </div>

              <h4 className="text-base font-extrabold text-slate-900 leading-tight">
                {rel.isNumber}
              </h4>
              <div className="text-xs font-semibold text-teal-700 mt-0.5">
                {rel.title}
              </div>

              <p className="text-xs text-slate-600 mt-3 leading-relaxed">
                {rel.description}
              </p>
            </div>

            <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs">
              <span className="text-slate-400 font-medium">Normative Status: Active</span>
              <button className="text-teal-600 font-bold hover:underline flex items-center gap-1">
                <span>View Clause</span>
                <ArrowUpRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Informational callout */}
      <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 text-xs text-slate-600 flex items-center justify-between">
        <span>Graph traversal ensures procurement tenders do not miss mandatory laboratory test protocols or prerequisite raw material certifications.</span>
        <span className="font-bold text-slate-800">Total Linked Nodes: {relatedList.length + 1}</span>
      </div>

    </div>
  );
}
