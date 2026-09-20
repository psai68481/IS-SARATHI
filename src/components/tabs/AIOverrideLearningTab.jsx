import React from 'react';
import { 
  BrainCircuit, 
  UserCheck, 
  Bot, 
  Sparkles, 
  Zap, 
  Lightbulb, 
  CheckCircle 
} from 'lucide-react';

export default function AIOverrideLearningTab({ data }) {
  const overrides = (data.historicalDecisions || []).filter(
    (item) => item.aiRecommendation !== item.humanDecision
  );

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-200 pb-4">
        <div>
          <h2 className="text-xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
            <BrainCircuit className="w-5 h-5 text-teal-600" />
            AI Override Analysis & Continual Learning Loop
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Feedback distillation system that converts procurement officer manual overrides into active retrieval training signals.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold px-2.5 py-1 bg-purple-50 text-purple-800 border border-purple-200 rounded-md flex items-center gap-1">
            <Sparkles className="w-3 h-3 text-purple-600" />
            {overrides.length} Active Override Signal(s)
          </span>
        </div>
      </div>

      {/* Override Comparative Cases */}
      <div className="space-y-6">
        {overrides.map((item, idx) => (
          <div 
            key={idx}
            className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden"
          >
            {/* Top Bar with Case info */}
            <div className="bg-slate-900 text-white px-5 sm:px-6 py-3.5 flex flex-wrap items-center justify-between gap-2">
              <div className="flex items-center gap-3">
                <span className="font-mono font-bold text-teal-300 text-sm">
                  {item.caseId}
                </span>
                <span className="text-slate-400">&bull;</span>
                <span className="text-xs font-semibold text-slate-200">
                  {item.title}
                </span>
              </div>

              <div className="flex items-center gap-2 text-xs">
                <span className="text-slate-400">{item.department}</span>
                <span className="bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-[10px] font-bold px-2 py-0.5 rounded-full uppercase">
                  Validated Override
                </span>
              </div>
            </div>

            {/* Before / After Comparison Grid */}
            <div className="p-5 sm:p-6 grid grid-cols-1 lg:grid-cols-2 gap-6">
              
              {/* Left: Original AI Recommendation */}
              <div className="bg-slate-50 rounded-xl p-5 border border-slate-200 space-y-3 relative">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold uppercase tracking-wider text-slate-500 flex items-center gap-1.5">
                    <Bot className="w-4 h-4 text-blue-600" />
                    AI Initial Recommendation
                  </span>
                  <span className="text-xs font-semibold text-blue-700 bg-blue-50 px-2 py-0.5 rounded border border-blue-200">
                    Baseline Output
                  </span>
                </div>

                <div className="text-xl font-extrabold text-slate-800 font-mono">
                  {item.aiRecommendation}
                </div>

                <p className="text-xs text-slate-600 leading-relaxed">
                  Generated purely based on semantic lexical overlap of "industrial safety helmet" and Clause 5.2 impact ratings without factoring high-voltage extreme environmental notes.
                </p>
              </div>

              {/* Right: Human Procurement Officer Decision */}
              <div className="bg-purple-50/70 rounded-xl p-5 border border-purple-200 space-y-3 relative">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold uppercase tracking-wider text-purple-900 flex items-center gap-1.5">
                    <UserCheck className="w-4 h-4 text-purple-700" />
                    Procurement Officer Final Decision
                  </span>
                  <span className="text-xs font-bold text-purple-800 bg-purple-100 px-2 py-0.5 rounded border border-purple-300">
                    Human Approved
                  </span>
                </div>

                <div className="text-xl font-extrabold text-purple-950 font-mono">
                  {item.humanDecision}
                </div>

                <p className="text-xs text-purple-900 font-medium leading-relaxed">
                  <strong>Override Justification: </strong>
                  {item.reason}
                </p>
              </div>

            </div>

            {/* Bottom: Distilled AI Learning Signal Box */}
            <div className="bg-gradient-to-r from-teal-900 via-slate-900 to-[#1E2761] text-white p-5 sm:p-6 border-t border-slate-200">
              <div className="flex items-start gap-4">
                <div className="w-10 h-10 rounded-xl bg-teal-500/20 border border-teal-400/30 flex items-center justify-center shrink-0">
                  <Lightbulb className="w-5 h-5 text-teal-300 animate-pulse" />
                </div>

                <div className="space-y-2 flex-1">
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <h4 className="text-sm font-bold text-teal-200 flex items-center gap-2">
                      <Zap className="w-4 h-4 text-amber-400" />
                      Synthesized AI Learning Signal & Prompt Adjustment
                    </h4>
                    <span className="text-[11px] font-mono text-slate-400 bg-black/40 px-2 py-0.5 rounded">
                      Policy Rule: #RL-2024-HV-01
                    </span>
                  </div>

                  <div className="bg-black/30 rounded-lg p-3.5 border border-white/10 text-xs text-slate-200 font-mono leading-relaxed">
                    <strong className="text-teal-300">RULE UPDATE: </strong>
                    When tender specification mentions high-voltage substation (&gt;11kV) or power transmission environments alongside general PPE requirements, prioritize IEC/ISO harmonized standard <strong>IS 15298 (Part 2)</strong> and enforce dielectric test validation over standard IS 2925 baseline.
                  </div>

                  <div className="pt-2 flex flex-wrap items-center justify-between gap-2 text-xs text-slate-300">
                    <span className="flex items-center gap-1.5">
                      <CheckCircle className="w-4 h-4 text-emerald-400" />
                      Weighting adjustment applied to Vector Reranker
                    </span>
                    <span className="text-teal-300 font-semibold">
                      Future Accuracy Expected: +3.8%
                    </span>
                  </div>
                </div>
              </div>
            </div>

          </div>
        ))}
      </div>

      {/* Model Continuous Improvement Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-bold text-slate-500 uppercase tracking-wider">
            Total Overrides Processed
          </div>
          <div className="text-2xl font-extrabold text-slate-900 mt-1 font-sans">
            3 Cases (6.4%)
          </div>
          <div className="text-xs text-emerald-600 mt-1 font-semibold">
            &darr; Reduced from 14% in v1.0
          </div>
        </div>

        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-bold text-slate-500 uppercase tracking-wider">
            Active Reinforcement Rules
          </div>
          <div className="text-2xl font-extrabold text-teal-700 mt-1 font-sans">
            18 Domain Rules
          </div>
          <div className="text-xs text-slate-500 mt-1">
            Governing high-voltage & mining PPE
          </div>
        </div>

        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-bold text-slate-500 uppercase tracking-wider">
            Human Agreement Index
          </div>
          <div className="text-2xl font-extrabold text-emerald-600 mt-1 font-sans">
            93.6%
          </div>
          <div className="text-xs text-slate-500 mt-1">
            Evaluator consensus rate
          </div>
        </div>
      </div>

    </div>
  );
}
