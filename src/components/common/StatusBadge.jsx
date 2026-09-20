import React from 'react';
import { CheckCircle2, XCircle, Award, Bookmark } from 'lucide-react';

export function StandardTypeBadge({ type }) {
  if (type === "Primary Standard") {
    return (
      <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-blue-50 text-blue-700 border border-blue-200">
        <Award className="w-3.5 h-3.5 text-blue-600" />
        Primary Standard
      </span>
    );
  }
  return (
    <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-purple-50 text-purple-700 border border-purple-200">
      <Bookmark className="w-3.5 h-3.5 text-purple-600" />
      Related Standard
    </span>
  );
}

export function StatusBadge({ status }) {
  const isCurrent = status === "Current";
  return (
    <span
      className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-xs font-medium border ${
        isCurrent
          ? "bg-emerald-50 text-emerald-700 border-emerald-200"
          : "bg-rose-50 text-rose-700 border-rose-200"
      }`}
    >
      <span className={`w-1.5 h-1.5 rounded-full ${isCurrent ? "bg-emerald-500" : "bg-rose-500"}`} />
      {status}
    </span>
  );
}

export function CertificationBadge({ certification }) {
  if (!certification || certification.status === "N/A") {
    return (
      <span className="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium bg-slate-100 text-slate-600 border border-slate-200">
        Voluntary / Scheme N/A
      </span>
    );
  }

  const isMandatory = certification.status === "Mandatory";
  return (
    <span
      className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-md text-xs font-semibold border ${
        isMandatory
          ? "bg-amber-50 text-amber-800 border-amber-300"
          : "bg-slate-100 text-slate-700 border-slate-200"
      }`}
    >
      <span className={`w-2 h-2 rounded-full ${isMandatory ? "bg-amber-500 animate-pulse" : "bg-slate-400"}`} />
      {certification.status}: {certification.scheme}
    </span>
  );
}
