import React, { useState } from 'react';
import { 
  GitFork, 
  Layers, 
  Award, 
  FlaskConical, 
  ShieldAlert, 
  Atom, 
  ExternalLink, 
  Info,
  CheckCircle,
  FileText,
  CornerDownRight
} from 'lucide-react';
import ConfidenceBadge from '../common/ConfidenceBadge';

export default function RelatedStandardsTab({ data }) {
  const topRec = data.recommendations[0];
  const relatedList = topRec.relatedStandards || [];
  const [selectedNode, setSelectedNode] = useState(relatedList[0] || null);

  const getNodeIcon = (type) => {
    switch (type) {
      case "Test Method":
        return <FlaskConical className="w-4 h-4 text-amber-600" />;
      case "Safety Standard":
        return <ShieldAlert className="w-4 h-4 text-blue-600" />;
      case "Material Standard":
        return <Atom className="w-4 h-4 text-purple-600" />;
      default:
        return <FileText className="w-4 h-4 text-teal-600" />;
    }
  };

  const getNodeBadgeClass = (type) => {
    switch (type) {
      case "Test Method":
        return "bg-amber-50 text-amber-700 border-amber-200";
      case "Safety Standard":
        return "bg-blue-50 text-blue-700 border-blue-200";
      case "Material Standard":
        return "bg-purple-50 text-purple-700 border-purple-200";
      default:
        return "bg-slate-50 text-slate-700 border-slate-200";
    }
  };

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-200 pb-4">
        <div>
          <h2 className="text-xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
            <GitFork className="w-5 h-5 text-teal-600" />
            Standards Dependency & Cross-Reference Graph
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Interconnected standards ecosystem linking primary specifications to mandatory test protocols and raw material grades.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold px-2.5 py-1 bg-white border border-slate-200 text-slate-700 rounded-md">
            Hub: <strong>{topRec.isNumber}</strong>
          </span>
        </div>
      </div>

      {/* Visual Tree / Graph Area */}
      <div className="bg-slate-900 text-white rounded-2xl p-6 sm:p-8 shadow-md relative overflow-hidden">
        {/* Subtle grid background */}
        <div 
          className="absolute inset-0 opacity-10"
          style={{
            backgroundImage: "radial-gradient(#94A3B8 1px, transparent 1px)",
            backgroundSize: "24px 24px"
          }}
        />

        <div className="relative z-10">
          <div className="flex items-center justify-between mb-6">
            <div className="text-xs font-bold uppercase tracking-wider text-teal-400 flex items-center gap-2">
              <Layers className="w-4 h-4" />
              Interactive Dependency Map
            </div>
            <span className="text-[11px] text-slate-400 bg-slate-800 px-2.5 py-1 rounded-full border border-slate-700">
              Click node to inspect clause links
            </span>
          </div>

          {/* Desktop/Tablet Node Graph Layout */}
          <div className="grid grid-cols-1 md:grid-cols-12 gap-6 items-center">
            
            {/* Center / Left Hub: Primary Standard Node */}
            <div className="md:col-span-5 flex flex-col items-center">
              <div className="w-full bg-gradient-to-br from-[#1E2761] to-[#028090] p-6 rounded-2xl border-2 border-teal-400 shadow-xl relative">
                <div className="absolute -top-3 left-4 bg-teal-400 text-slate-950 font-extrabold text-[10px] uppercase tracking-wider px-2.5 py-0.5 rounded-full shadow">
                  Root Specification Hub
                </div>

                <div className="flex items-start justify-between">
                  <div>
                    <h3 className="text-2xl font-black text-white tracking-tight">
                      {topRec.isNumber}
                    </h3>
                    <p className="text-xs font-bold text-teal-200 mt-1">
                      {topRec.title}
                    </p>
                  </div>
                  <Award className="w-7 h-7 text-teal-300 shrink-0" />
                </div>

                <p className="text-xs text-slate-200 mt-3 leading-relaxed">
                  Primary standard governing construction, shell retention, dielectric insulation, and shock absorption.
                </p>

                <div className="mt-4 pt-3 border-t border-white/20 flex items-center justify-between text-xs">
                  <span className="text-teal-200 font-semibold">BIS ISI Mandatory</span>
                  <span className="text-white font-bold bg-white/10 px-2 py-0.5 rounded">91% Match</span>
                </div>
              </div>
            </div>

            {/* Connecting Visual SVG Indicators / Arrows */}
            <div className="hidden md:flex md:col-span-1 flex-col items-center justify-center space-y-8 text-teal-400">
              <div className="w-full h-0.5 bg-gradient-to-r from-teal-400 to-amber-400 relative">
                <div className="absolute right-0 -top-1 w-2 h-2 border-t-2 border-r-2 border-amber-400 rotate-45"></div>
              </div>
              <div className="w-full h-0.5 bg-gradient-to-r from-teal-400 to-blue-400 relative">
                <div className="absolute right-0 -top-1 w-2 h-2 border-t-2 border-r-2 border-blue-400 rotate-45"></div>
              </div>
              <div className="w-full h-0.5 bg-gradient-to-r from-teal-400 to-purple-400 relative">
                <div className="absolute right-0 -top-1 w-2 h-2 border-t-2 border-r-2 border-purple-400 rotate-45"></div>
              </div>
            </div>

            {/* Right Leaves: Related Standards Nodes */}
            <div className="md:col-span-6 space-y-3">
              {relatedList.map((item, idx) => {
                const isSelected = selectedNode?.isNumber === item.isNumber;
                return (
                  <div
                    key={idx}
                    onClick={() => setSelectedNode(item)}
                    className={`cursor-pointer p-4 rounded-xl border transition-all duration-200 ${
                      isSelected
                        ? "bg-slate-800 border-teal-400 shadow-lg ring-1 ring-teal-400"
                        : "bg-slate-800/60 border-slate-700 hover:bg-slate-800 hover:border-slate-500"
                    }`}
                  >
                    <div className="flex items-center justify-between mb-1.5">
                      <div className="flex items-center gap-2">
                        {getNodeIcon(item.type)}
                        <span className={`text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded border ${getNodeBadgeClass(item.type)}`}>
                          {item.type}
                        </span>
                      </div>
                      <span className="text-xs font-mono font-bold text-teal-300">
                        {item.isNumber}
                      </span>
                    </div>

                    <h4 className="text-sm font-bold text-white">
                      {item.title}
                    </h4>

                    <p className="text-xs text-slate-400 mt-1 line-clamp-2">
                      {item.description}
                    </p>
                  </div>
                );
              })}
            </div>

          </div>
        </div>
      </div>

      {/* Selected Node Deep Dive Details Panel */}
      {selectedNode && (
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-xs">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3 mb-4">
            <div className="flex items-center gap-2">
              <Info className="w-4 h-4 text-teal-600" />
              <h3 className="text-sm font-bold text-slate-900">
                Detailed Linkage Breakdown: <span className="text-teal-700">{selectedNode.isNumber}</span>
              </h3>
            </div>
            <span className={`text-xs font-semibold px-2.5 py-0.5 rounded-full border ${getNodeBadgeClass(selectedNode.type)}`}>
              {selectedNode.type}
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
            <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
              <span className="font-bold text-slate-500 block uppercase text-[10px]">Standard Title</span>
              <span className="font-semibold text-slate-800 mt-1 block">{selectedNode.title}</span>
            </div>

            <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
              <span className="font-bold text-slate-500 block uppercase text-[10px]">Relationship to IS 2925</span>
              <span className="font-semibold text-slate-800 mt-1 block">
                {selectedNode.type === "Test Method" 
                  ? "Normative reference for Clause 5.2 Drop Tower calibration" 
                  : selectedNode.type === "Material Standard" 
                  ? "Raw resin HDPE polymer melt-flow index validation" 
                  : "Harmonized occupational ergonomics classification"}
              </span>
            </div>

            <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
              <span className="font-bold text-slate-500 block uppercase text-[10px]">Procurement Audit Note</span>
              <span className="font-semibold text-slate-800 mt-1 block">
                Vendor test certificates must cite testing conducted under this standard.
              </span>
            </div>
          </div>
        </div>
      )}

    </div>
  );
}
