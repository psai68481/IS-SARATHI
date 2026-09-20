import React from 'react';
import { 
  Compass, 
  FileDown, 
  Layers, 
  Menu,
  X
} from 'lucide-react';

export default function Topbar({ 
  activePreset, 
  onSelectPreset, 
  presets = [], 
  onExportReport,
  isMobileSidebarOpen,
  setIsMobileSidebarOpen
}) {
  return (
    <header className="bg-white border-b border-slate-200 sticky top-0 z-30 shadow-sm">
      <div className="px-4 sm:px-6 py-3 flex items-center justify-between gap-3">
        
        {/* Left: Hamburger (Mobile) + Brand Identity */}
        <div className="flex items-center gap-3">
          <button
            onClick={() => setIsMobileSidebarOpen(!isMobileSidebarOpen)}
            className="md:hidden p-2 rounded-lg text-slate-600 hover:bg-slate-100 border border-slate-200"
            aria-label="Toggle Navigation Menu"
          >
            {isMobileSidebarOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>

          <div className="flex items-center gap-2.5 sm:gap-3">
            <div className="w-9 h-9 sm:w-10 sm:h-10 rounded-xl bg-gradient-to-tr from-[#1E2761] to-[#028090] flex items-center justify-center text-white shadow-md">
              <Compass className="w-5 h-5 sm:w-6 sm:h-6 text-teal-200" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-extrabold text-lg sm:text-xl tracking-tight text-slate-900 font-sans">
                  IS-SARATHI
                </span>
                <span className="bg-teal-50 text-teal-700 text-[10px] sm:text-[11px] font-bold px-2 py-0.5 rounded border border-teal-200 uppercase tracking-wider">
                  BIS AI Engine
                </span>
              </div>
              <p className="hidden sm:block text-[11px] text-slate-500 font-medium">
                AI-Powered Indian Standards Recommendation System for Procurement
              </p>
            </div>
          </div>
        </div>

        {/* Center: Tender Preset Switcher (Hidden on small screens) */}
        <div className="hidden xl:flex items-center gap-2 bg-slate-100 p-1 rounded-lg border border-slate-200">
          <span className="text-xs font-semibold text-slate-500 px-2 flex items-center gap-1.5">
            <Layers className="w-3.5 h-3.5 text-slate-400" />
            Active Tender Case:
          </span>
          <select
            value={activePreset}
            onChange={(e) => onSelectPreset(e.target.value)}
            className="bg-white text-xs font-medium text-slate-800 py-1 pl-3 pr-8 rounded border border-slate-200 focus:outline-none focus:ring-1 focus:ring-teal-500 cursor-pointer shadow-sm"
          >
            {presets.map((p) => (
              <option key={p.id} value={p.id}>
                {p.title}
              </option>
            ))}
          </select>
        </div>

        {/* Right: Demo Mode & Export Report */}
        <div className="flex items-center gap-2 sm:gap-3">
          {/* Demo Mode Badge */}
          <div className="flex items-center gap-1.5 sm:gap-2 px-2.5 sm:px-3 py-1 sm:py-1.5 rounded-full bg-amber-50 border border-amber-200 text-amber-800 shadow-sm">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-amber-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-amber-500"></span>
            </span>
            <span className="text-[11px] sm:text-xs font-bold tracking-tight">
              Demo Mode
            </span>
          </div>

          {/* Export Report Action */}
          <button
            onClick={onExportReport}
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-[#028090] hover:bg-[#006d7b] text-white shadow-sm transition-all duration-150 active:scale-95"
            title="Download Procurement Recommendation Summary"
          >
            <FileDown className="w-4 h-4" />
            <span className="hidden sm:inline">Export Report</span>
          </button>

          {/* User profile / agency info */}
          <div className="hidden md:flex items-center gap-2 pl-2 border-l border-slate-200">
            <div className="w-8 h-8 rounded-full bg-[#1E2761] text-white flex items-center justify-center font-bold text-xs shadow-sm">
              GOV
            </div>
            <div className="text-left leading-tight">
              <div className="text-xs font-semibold text-slate-800">GeM Portal</div>
              <div className="text-[10px] text-slate-400">Technical Auditor</div>
            </div>
          </div>
        </div>

      </div>
    </header>
  );
}
