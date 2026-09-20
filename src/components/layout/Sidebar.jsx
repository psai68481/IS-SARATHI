import React from 'react';
import {
  LayoutDashboard,
  FileText,
  Bot,
  GitFork,
  CheckSquare,
  AlertTriangle,
  HelpCircle,
  History,
  BrainCircuit,
  Shield,
  Sparkles,
  X
} from 'lucide-react';

export const TABS = [
  { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard, badge: null },
  { id: 'tender-analysis', label: 'Tender Analysis', icon: FileText, badge: '4' },
  { id: 'recommendations', label: 'AI Recommendations', icon: Bot, badge: '91%' },
  { id: 'related-standards', label: 'Related Standards', icon: GitFork, badge: '3' },
  { id: 'coverage', label: 'Requirement Coverage', icon: CheckSquare, badge: '75%' },
  { id: 'conflicts-gaps', label: 'Conflicts & Gaps', icon: AlertTriangle, badge: '1 Flag', alert: true },
  { id: 'why-not', label: 'Why Not?', icon: HelpCircle, badge: '3' },
  { id: 'history', label: 'Historical Decisions', icon: History, badge: '5' },
  { id: 'learning', label: 'AI Override & Learning', icon: BrainCircuit, badge: '1 Signal' },
];

export default function Sidebar({ activeTab, onSelectTab, isOpen, onClose }) {
  const handleTabClick = (tabId) => {
    onSelectTab(tabId);
    if (onClose) {
      onClose();
    }
  };

  return (
    <>
      {/* Mobile Backdrop Overlay */}
      {isOpen && (
        <div
          onClick={onClose}
          className="fixed inset-0 bg-black/60 z-40 md:hidden backdrop-blur-sm transition-opacity"
        />
      )}

      <aside
        className={`w-64 sm:w-72 bg-[#1E2761] text-slate-100 flex flex-col justify-between shrink-0 select-none transition-transform duration-300 z-50
          fixed md:sticky top-0 md:top-[61px] h-screen md:h-[calc(100vh-61px)]
          ${isOpen ? "translate-x-0" : "-translate-x-full md:translate-x-0"}
        `}
      >
        {/* Navigation Links Area */}
        <div className="p-3 sm:p-4 space-y-4 overflow-y-auto">
          
          {/* Mobile Top Close Row */}
          <div className="flex md:hidden items-center justify-between pb-2 border-b border-white/10">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-300">
              Navigation Menu
            </span>
            <button
              onClick={onClose}
              className="p-1 rounded-md text-slate-400 hover:text-white hover:bg-white/10"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Section Header */}
          <div>
            <div className="px-3 text-[11px] font-bold tracking-wider text-slate-400 uppercase mb-2">
              Procurement Workflow
            </div>
            <nav className="space-y-1">
              {TABS.map((tab) => {
                const Icon = tab.icon;
                const isActive = activeTab === tab.id;

                return (
                  <button
                    key={tab.id}
                    onClick={() => handleTabClick(tab.id)}
                    className={`w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-150 text-left group ${
                      isActive
                        ? "bg-[#028090] text-white shadow-md font-semibold"
                        : "text-slate-300 hover:bg-white/10 hover:text-white"
                    }`}
                  >
                    <div className="flex items-center gap-3 min-w-0 flex-1 pr-2">
                      <Icon className={`w-4 h-4 shrink-0 transition-transform group-hover:scale-110 ${
                        isActive ? "text-white" : "text-slate-400 group-hover:text-slate-200"
                      }`} />
                      <span className="truncate text-xs sm:text-sm">{tab.label}</span>
                    </div>

                    {tab.badge && (
                      <span
                        className={`shrink-0 whitespace-nowrap text-[10px] px-2 py-0.5 rounded-full font-bold uppercase tracking-tight ${
                          isActive
                            ? "bg-white/20 text-white"
                            : tab.alert
                            ? "bg-amber-500/20 text-amber-300 border border-amber-500/30"
                            : "bg-slate-700/80 text-slate-300 border border-slate-600"
                        }`}
                      >
                        {tab.badge}
                      </span>
                    )}
                  </button>
                );
              })}
            </nav>
          </div>

          {/* Standards Registry Card */}
          <div className="bg-white/5 border border-white/10 rounded-xl p-3.5 text-xs text-slate-300">
            <div className="flex items-center gap-2 text-white font-semibold mb-1">
              <Shield className="w-4 h-4 text-teal-400 shrink-0" />
              <span>BIS Standards Index</span>
            </div>
            <p className="text-[11px] text-slate-400 leading-relaxed">
              Mapped with Bureau of Indian Standards (BIS) e-Sale Catalog & Quality Control Orders.
            </p>
            <div className="mt-2.5 pt-2 border-t border-white/10 flex items-center justify-between text-[10px] text-slate-400">
              <span>Status: <strong className="text-emerald-400">Active</strong></span>
              <span>v2024.3</span>
            </div>
          </div>

        </div>

        {/* Footer info */}
        <div className="p-3 sm:p-4 border-t border-white/10 bg-slate-900/40 text-[11px] text-slate-400">
          <div className="flex items-center gap-2 mb-1 text-slate-300 font-medium">
            <Sparkles className="w-3.5 h-3.5 text-teal-400 shrink-0" />
            <span>Smart India Hackathon</span>
          </div>
          <p className="text-[10px] text-slate-400 leading-tight">
            IS-SARATHI AI Prototype for Automated Standard Alignment.
          </p>
        </div>
      </aside>
    </>
  );
}
