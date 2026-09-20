import React from 'react';
import { ShieldCheck, ShieldAlert, AlertTriangle } from 'lucide-react';

export default function ConfidenceBadge({ score, size = "md", showIcon = true }) {
  let colorClasses = "";
  let icon = null;

  if (score >= 90) {
    colorClasses = "bg-emerald-50 text-emerald-700 border-emerald-200 ring-emerald-500/20";
    icon = <ShieldCheck className={size === "lg" ? "w-4 h-4" : size === "sm" ? "w-3 h-3" : "w-3.5 h-3.5"} />;
  } else if (score >= 70) {
    colorClasses = "bg-amber-50 text-amber-700 border-amber-200 ring-amber-500/20";
    icon = <AlertTriangle className={size === "lg" ? "w-4 h-4" : size === "sm" ? "w-3 h-3" : "w-3.5 h-3.5"} />;
  } else {
    colorClasses = "bg-rose-50 text-rose-700 border-rose-200 ring-rose-500/20";
    icon = <ShieldAlert className={size === "lg" ? "w-4 h-4" : size === "sm" ? "w-3 h-3" : "w-3.5 h-3.5"} />;
  }

  const sizeClasses = {
    sm: "text-xs px-2 py-0.5 font-medium gap-1",
    md: "text-xs px-2.5 py-1 font-semibold gap-1.5",
    lg: "text-sm px-3.5 py-1.5 font-bold gap-2"
  }[size] || "text-xs px-2.5 py-1 font-semibold gap-1.5";

  return (
    <span className={`inline-flex items-center rounded-full border shadow-sm ${sizeClasses} ${colorClasses}`}>
      {showIcon && icon}
      <span>{score}% Match</span>
    </span>
  );
}
