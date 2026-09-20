import React from 'react';

interface StatusBadgeProps {
  status: string;
}

export default function StatusBadge({ status }: StatusBadgeProps) {
  const norm = (status || '').toUpperCase();
  let bg = 'bg-slate-100 text-slate-700 border-slate-300';

  if (norm.includes('CURRENT') || norm.includes('ACTIVE')) {
    bg = 'bg-emerald-50 text-emerald-800 border-emerald-300';
  } else if (norm.includes('REAFFIRMED')) {
    bg = 'bg-teal-50 text-teal-800 border-teal-300';
  } else if (norm.includes('SUPERSEDED')) {
    bg = 'bg-amber-50 text-amber-800 border-amber-300';
  } else if (norm.includes('WITHDRAWN')) {
    bg = 'bg-rose-50 text-rose-800 border-rose-300';
  }

  return (
    <span className={`inline-flex items-center text-[10px] font-bold px-2 py-0.5 rounded border uppercase tracking-wider ${bg}`}>
      {status || 'Current'}
    </span>
  );
}
