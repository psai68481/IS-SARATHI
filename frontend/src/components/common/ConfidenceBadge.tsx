import React from 'react';

interface ConfidenceBadgeProps {
  score: number;
  size?: 'sm' | 'md' | 'lg';
}

export default function ConfidenceBadge({ score, size = 'md' }: ConfidenceBadgeProps) {
  let colorClasses = 'bg-emerald-50 text-emerald-700 border-emerald-300';
  let dotColor = 'bg-emerald-500';
  let tierLabel = 'High Confidence';

  if (score < 70) {
    colorClasses = 'bg-rose-50 text-rose-700 border-rose-300';
    dotColor = 'bg-rose-500';
    tierLabel = 'Review Needed';
  } else if (score < 80) {
    colorClasses = 'bg-amber-50 text-amber-700 border-amber-300';
    dotColor = 'bg-amber-500';
    tierLabel = 'Moderate';
  } else if (score < 90) {
    colorClasses = 'bg-teal-50 text-teal-700 border-teal-300';
    dotColor = 'bg-teal-500';
    tierLabel = 'Optimal';
  }

  const sizeClasses = {
    sm: 'text-[11px] px-2 py-0.5',
    md: 'text-xs px-2.5 py-1',
    lg: 'text-sm px-3.5 py-1.5',
  }[size];

  return (
    <span
      className={`inline-flex items-center gap-1.5 font-bold rounded-full border shadow-sm ${colorClasses} ${sizeClasses}`}
    >
      <span className={`w-1.5 h-1.5 rounded-full ${dotColor} animate-pulse`} />
      <span>{score}% Confidence</span>
      {size !== 'sm' && <span className="opacity-70 font-normal">({tierLabel})</span>}
    </span>
  );
}
