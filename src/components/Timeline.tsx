import React from "react";

export type TimelineStep = {
  id: string;
  label: string;
  date: string;
  status: "completed" | "current" | "pending";
};

interface TimelineProps {
  steps: TimelineStep[];
}

export function Timeline({ steps }: TimelineProps) {
  return (
    <div className="w-full">
      <h2 className="text-[20px] leading-[28px] font-semibold text-primary mb-6">
        Election Journey
      </h2>
      <div className="relative flex items-center justify-between w-full">
        {/* Background Track */}
        <div className="absolute top-1/2 left-0 w-full h-[2px] bg-surface-variant -z-10 -translate-y-1/2" />

        {/* Steps */}
        {steps.map((step, index) => {
          const isCompleted = step.status === "completed";
          const isCurrent = step.status === "current";
          
          return (
            <div key={step.id} className="flex flex-col items-center relative group">
              {/* Progress Track Overlay (up to current) */}
              {index > 0 && (isCompleted || isCurrent) && (
                <div 
                  className="absolute top-1/2 right-1/2 w-[200%] h-[2px] bg-secondary -z-10 -translate-y-1/2" 
                />
              )}

              {/* Indicator Pill/Circle */}
              <div
                className={`flex items-center justify-center h-8 w-8 rounded-full mb-3 transition-colors ${
                  isCompleted
                    ? "bg-secondary text-white"
                    : isCurrent
                    ? "bg-secondary text-white ring-4 ring-secondary/20"
                    : "bg-surface-variant text-on-surface-variant"
                }`}
              >
                {isCompleted ? (
                  <svg
                    className="w-4 h-4"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2.5}
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                ) : (
                  <span className="text-[12px] font-medium">{index + 1}</span>
                )}
              </div>

              {/* Text Information */}
              <div className="flex flex-col items-center text-center max-w-[120px]">
                <span
                  className={`text-[14px] leading-[20px] font-semibold mb-1 ${
                    isCompleted || isCurrent ? "text-primary" : "text-outline"
                  }`}
                  style={{ letterSpacing: "0.02em" }}
                >
                  {step.label}
                </span>
                <span className="text-[12px] leading-[16px] font-medium text-on-surface-variant">
                  {step.date}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
