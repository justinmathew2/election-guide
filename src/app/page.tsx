"use client";

import { useEffect, useState } from "react";
import { Timeline, TimelineStep } from "@/components/Timeline";

const API_BASE_URL = "https://election-guide-backend-927623157898.us-central1.run.app/api";

export default function Home() {
  const [journeyState, setJourneyState] = useState<string>("NOT_STARTED");
  const [zkpResult, setZkpResult] = useState<{ is_eligible: boolean; message: string; zkp_proof?: string } | null>(null);

  // Sync state from backend
  const fetchState = async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/journey/state`);
      const data = await res.json();
      setJourneyState(data.state);
    } catch (error) {
      console.error("Failed to fetch journey state", error);
    }
  };

  useEffect(() => {
    fetchState();
  }, []);

  const advanceJourney = async () => {
    try {
      await fetch(`${API_BASE_URL}/journey/advance`, { method: "POST" });
      fetchState();
    } catch (error) {
      console.error("Failed to advance journey", error);
    }
  };

  const verifyEligibility = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    try {
      const res = await fetch(`${API_BASE_URL}/journey/verify-eligibility`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          age: Number(formData.get("age")),
          location: formData.get("location"),
        }),
      });
      const data = await res.json();
      setZkpResult(data);
    } catch (error) {
      console.error("Failed to verify eligibility", error);
    }
  };

  // Map backend state to frontend timeline
  const electionSteps: TimelineStep[] = [
    { id: "1", label: "Registration", date: "Step 1", status: journeyState === "NOT_STARTED" ? "pending" : (journeyState === "REGISTRATION" ? "current" : "completed") },
    { id: "2", label: "Primary", date: "Step 2", status: ["NOT_STARTED", "REGISTRATION"].includes(journeyState) ? "pending" : (journeyState === "PRIMARY" ? "current" : "completed") },
    { id: "3", label: "General Election", date: "Step 3", status: ["COMPLETED", "GENERAL_ELECTION"].includes(journeyState) ? (journeyState === "GENERAL_ELECTION" ? "current" : "completed") : "pending" },
  ];

  return (
    <main className="min-h-screen bg-background p-8 sm:p-24 flex flex-col items-center">
      <div className="w-full max-w-4xl flex flex-col gap-12 bg-surface-container-lowest p-8 sm:p-12 rounded-2xl shadow-ambient">
        <div className="text-center">
          <h1 className="text-[32px] leading-[40px] font-bold text-primary mb-4 tracking-[-0.02em]">
            Civic Clarity: Election Guide
          </h1>
          <p className="text-[18px] leading-[28px] text-on-surface-variant max-w-2xl mx-auto">
            Your trusted guide for official election data and deadlines. Ensure your voice is heard by following the journey below.
          </p>
        </div>

        <section className="bg-surface-container-low p-8 rounded-xl border border-surface-variant/50">
          <Timeline steps={electionSteps} />
          
          <div className="mt-8 flex justify-center">
             <button 
                onClick={advanceJourney}
                className="h-[48px] px-6 bg-secondary text-white font-semibold rounded-lg hover:bg-secondary-container transition-colors shadow-ambient"
             >
                Advance Journey State
             </button>
          </div>
        </section>

        <section className="bg-surface-container-low p-8 rounded-xl border border-surface-variant/50">
          <h2 className="text-[20px] font-semibold text-primary mb-4">ZKP Eligibility Verification</h2>
          <form onSubmit={verifyEligibility} className="flex flex-col sm:flex-row gap-4 items-end">
            <div className="flex-1">
              <label className="block text-sm font-medium text-on-surface mb-1">Age</label>
              <input type="number" name="age" required className="w-full h-[40px] px-3 rounded-md border border-outline-variant bg-surface-container-lowest text-on-surface focus:outline-none focus:ring-2 focus:ring-primary" />
            </div>
            <div className="flex-1">
              <label className="block text-sm font-medium text-on-surface mb-1">Location</label>
              <input type="text" name="location" required className="w-full h-[40px] px-3 rounded-md border border-outline-variant bg-surface-container-lowest text-on-surface focus:outline-none focus:ring-2 focus:ring-primary" />
            </div>
            <button type="submit" className="h-[40px] px-6 bg-primary text-white font-semibold rounded-lg hover:bg-primary-container transition-colors shadow-ambient">
              Verify
            </button>
          </form>
          
          {zkpResult && (
            <div className={`mt-4 p-4 rounded-md ${zkpResult.is_eligible ? 'bg-primary-fixed text-on-primary-fixed' : 'bg-error-container text-on-error-container'}`}>
              <p className="font-semibold">{zkpResult.message}</p>
              {zkpResult.zkp_proof && (
                <p className="text-xs mt-2 break-all opacity-80">Proof Hash: {zkpResult.zkp_proof}</p>
              )}
            </div>
          )}
        </section>
      </div>
    </main>
  );
}
