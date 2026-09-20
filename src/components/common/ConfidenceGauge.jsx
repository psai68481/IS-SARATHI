import React from 'react';

export default function ConfidenceGauge({ score = 91, size = 110, strokeWidth = 10, label = "AI Confidence" }) {
  // Determine color based on threshold
  let strokeColor = "#10B981"; // emerald green (>= 90)
  let textColor = "text-emerald-600";

  if (score >= 90) {
    strokeColor = "#10B981";
    textColor = "text-emerald-600";
  } else if (score >= 70) {
    strokeColor = "#F59E0B";
    textColor = "text-amber-600";
  } else {
    strokeColor = "#EF4444";
    textColor = "text-rose-600";
  }

  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  return (
    <div className="flex flex-col items-center justify-center">
      <div style={{ width: size, height: size }} className="relative flex items-center justify-center">
        <svg width={size} height={size} className="rotate-[-90deg]">
          {/* Background circle */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke="#E2E8F0"
            strokeWidth={strokeWidth}
            fill="transparent"
          />
          {/* Animated progress circle */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke={strokeColor}
            strokeWidth={strokeWidth}
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            fill="transparent"
            style={{ transition: "stroke-dashoffset 0.8s ease-in-out" }}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
          <span className={`text-xl font-extrabold tracking-tight ${textColor}`}>
            {score}%
          </span>
          <span className="text-[10px] font-semibold uppercase tracking-wider text-slate-400 -mt-0.5">
            Score
          </span>
        </div>
      </div>
      {label && (
        <span className="text-xs font-medium text-slate-500 mt-1">
          {label}
        </span>
      )}
    </div>
  );
}
