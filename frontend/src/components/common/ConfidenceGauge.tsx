import React from 'react';

interface ConfidenceGaugeProps {
  score: number;
}

export default function ConfidenceGauge({ score }: ConfidenceGaugeProps) {
  const radius = 38;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (score / 100) * circumference;

  let strokeColor = '#10B981'; // green
  if (score < 70) strokeColor = '#EF4444'; // red
  else if (score < 80) strokeColor = '#F59E0B'; // amber
  else if (score < 90) strokeColor = '#028090'; // teal

  return (
    <div className="relative inline-flex items-center justify-center">
      <svg className="w-24 h-24 transform -rotate-90">
        <circle
          cx="48"
          cy="48"
          r={radius}
          stroke="#E2E8F0"
          strokeWidth="8"
          fill="transparent"
        />
        <circle
          cx="48"
          cy="48"
          r={radius}
          stroke={strokeColor}
          strokeWidth="8"
          fill="transparent"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          className="transition-all duration-1000 ease-out"
        />
      </svg>
      <div className="absolute flex flex-col items-center justify-center text-center">
        <span className="text-xl font-black text-slate-900 font-sans">{score}%</span>
        <span className="text-[9px] font-bold text-slate-400 uppercase tracking-tight">Confidence</span>
      </div>
    </div>
  );
}
