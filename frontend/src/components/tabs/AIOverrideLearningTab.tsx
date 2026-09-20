import React, { useState } from 'react';
import { 
  BrainCircuit, 
  Send, 
  CheckCircle2, 
  ShieldCheck, 
  RefreshCw,
  Sparkles,
  AlertCircle
} from 'lucide-react';
import { DashboardData } from '@/types';
import { submitDecisionFeedbackApi } from '@/lib/api';

interface AIOverrideLearningTabProps {
  data: DashboardData;
}

export default function AIOverrideLearningTab({ data }: AIOverrideLearningTabProps) {
  const topRec = data.recommendations[0];
  const [selectedAction, setSelectedAction] = useState<'VALIDATE' | 'OVERRIDE' | 'REJECT'>('VALIDATE');
  const [customStandard, setCustomStandard] = useState('');
  const [justification, setJustification] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitSuccess, setSubmitSuccess] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!justification) return;

    setIsSubmitting(true);
    const feedbackPayload = {
      case_id: `PROC-${Math.floor(1000 + Math.random() * 9000)}`,
      title: 'Procurement Officer Case Verification',
      department: 'Public Works Department',
      tender_query: data.tenderQuery,
      ai_recommendation: topRec?.isNumber || 'Not available',
      ai_confidence: topRec?.confidence || 0,
      human_choice: selectedAction === 'OVERRIDE' ? customStandard : topRec?.isNumber || 'Not available',
      justification: justification,
      validation_status: selectedAction === 'VALIDATE' ? 'Validated' : (selectedAction === 'OVERRIDE' ? 'Validated' : 'Rejected')
    };

    try {
      await submitDecisionFeedbackApi(feedbackPayload);
      setSubmitSuccess(true);
      setTimeout(() => {
        setSubmitSuccess(false);
        setJustification('');
        setCustomStandard('');
      }, 3000);
    } catch (err) {
      console.warn('Error logging feedback:', err);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="space-y-6">
      
      {/* Header Info */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-200 pb-4">
        <div>
          <h2 className="text-xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
            <BrainCircuit className="w-5 h-5 text-teal-600" />
            Human-AI Governance & Feedback Loop
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Record officer validations, sign-offs, and structured overrides to refine re-ranking policies and maintain governance accountability.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold px-2.5 py-1 bg-teal-50 text-teal-700 rounded-md border border-teal-200">
            Safety Principle: AI Recommends &bull; Human Decides
          </span>
        </div>
      </div>

      {/* Main Feedback Form Card */}
      <div className="bg-white rounded-xl border border-slate-200 p-5 sm:p-6 shadow-sm space-y-5">
        <div>
          <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wide">
            Record Officer Determination
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            Active Tender: "{data.tenderQuery}"
          </p>
        </div>

        {/* Current AI Recommendation Banner */}
        <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block mb-0.5">
              AI Proposed Primary Standard
            </span>
            <span className="text-sm font-black text-slate-900">
              {topRec?.isNumber} &bull; {topRec?.title}
            </span>
          </div>
          <span className="text-xs font-bold text-teal-700 bg-teal-100 px-3 py-1 rounded-full border border-teal-200">
            {topRec?.confidence}% Confidence Score
          </span>
        </div>

        {/* Action Radio Toggle */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <button
              type="button"
              onClick={() => setSelectedAction('VALIDATE')}
              className={`p-3.5 rounded-xl border text-left transition-all ${
                selectedAction === 'VALIDATE'
                  ? 'border-emerald-500 bg-emerald-50/50 text-emerald-900 ring-2 ring-emerald-500/20'
                  : 'border-slate-200 hover:border-slate-300 text-slate-700'
              }`}
            >
              <div className="font-bold text-xs flex items-center gap-1.5 mb-1">
                <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                <span>Confirm & Validate</span>
              </div>
              <p className="text-[11px] text-slate-500 leading-tight">
                Accept AI recommendation as primary tender citation.
              </p>
            </button>

            <button
              type="button"
              onClick={() => setSelectedAction('OVERRIDE')}
              className={`p-3.5 rounded-xl border text-left transition-all ${
                selectedAction === 'OVERRIDE'
                  ? 'border-amber-500 bg-amber-50/50 text-amber-900 ring-2 ring-amber-500/20'
                  : 'border-slate-200 hover:border-slate-300 text-slate-700'
              }`}
            >
              <div className="font-bold text-xs flex items-center gap-1.5 mb-1">
                <ShieldCheck className="w-4 h-4 text-amber-600" />
                <span>Justified Override</span>
              </div>
              <p className="text-[11px] text-slate-500 leading-tight">
                Designate alternate or combo standard with rationale.
              </p>
            </button>

            <button
              type="button"
              onClick={() => setSelectedAction('REJECT')}
              className={`p-3.5 rounded-xl border text-left transition-all ${
                selectedAction === 'REJECT'
                  ? 'border-rose-500 bg-rose-50/50 text-rose-900 ring-2 ring-rose-500/20'
                  : 'border-slate-200 hover:border-slate-300 text-slate-700'
              }`}
            >
              <div className="font-bold text-xs flex items-center gap-1.5 mb-1">
                <AlertCircle className="w-4 h-4 text-rose-600" />
                <span>Flag for Re-Tender</span>
              </div>
              <p className="text-[11px] text-slate-500 leading-tight">
                Reject alignment due to contradictory requirements.
              </p>
            </button>
          </div>

          {/* Alternate Standard Input if Override */}
          {selectedAction === 'OVERRIDE' && (
            <div className="space-y-1.5">
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider">
                Alternate Indian Standard(s) Cited
              </label>
              <input
                type="text"
                value={customStandard}
                onChange={(e) => setCustomStandard(e.target.value)}
                placeholder="e.g. standard code + related test method"
                className="w-full text-xs sm:text-sm p-3 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500"
                required
              />
            </div>
          )}

          {/* Mandatory Justification Box */}
          <div className="space-y-1.5">
            <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider">
              Technical Justification / Officer Notes (Mandatory for Audit)
            </label>
            <textarea
              rows={3}
              value={justification}
              onChange={(e) => setJustification(e.target.value)}
              placeholder="State the site conditions, special dielectric requirements, or committee minutes supporting this determination..."
              className="w-full text-xs sm:text-sm p-3 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500"
              required
            />
          </div>

          {/* Submit Button */}
          <div className="flex items-center justify-between pt-2">
            <span className="text-xs text-slate-400">
              Logged into immutable GeM procurement audit trail.
            </span>

            <button
              type="submit"
              disabled={isSubmitting || !justification}
              className={`px-5 py-2.5 rounded-lg text-xs font-bold text-white shadow-sm flex items-center gap-2 transition-all active:scale-95 ${
                isSubmitting || !justification
                  ? 'bg-slate-400 cursor-not-allowed'
                  : 'bg-[#028090] hover:bg-[#006d7b]'
              }`}
            >
              {isSubmitting ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin" />
                  <span>Recording Decision...</span>
                </>
              ) : (
                <>
                  <Send className="w-4 h-4" />
                  <span>Submit Determination</span>
                </>
              )}
            </button>
          </div>

          {submitSuccess && (
            <div className="p-3 bg-emerald-50 border border-emerald-200 rounded-lg flex items-center gap-2 text-xs text-emerald-900 font-semibold animate-in fade-in">
              <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
              <span>Officer decision recorded successfully into PostgreSQL governance log and integrated into ranking policy calibration.</span>
            </div>
          )}
        </form>
      </div>

    </div>
  );
}
