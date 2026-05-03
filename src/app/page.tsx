"use client";

import { useState } from "react";
import useSWR, { mutate } from "swr";
import { motion, AnimatePresence } from "framer-motion";
import { Timeline, TimelineStep } from "@/components/Timeline";
import { ShieldCheck, ArrowRight, RefreshCw, Send, CheckCircle2, AlertCircle } from "lucide-react";

const API_BASE_URL = "https://election-guide-backend-927623157898.us-central1.run.app/api";

const fetcher = (url: string) => fetch(url).then((res) => res.json());

export default function Home() {
  const { data: stateData } = useSWR(`${API_BASE_URL}/journey/state`, fetcher, {
    refreshInterval: 5000,
  });
  
  const [zkpResult, setZkpResult] = useState<{ is_eligible: boolean; message: string; zkp_proof?: string } | null>(null);
  const [isVerifying, setIsVerifying] = useState(false);
  const [isAdvancing, setIsAdvancing] = useState(false);

  const journeyState = stateData?.state || "NOT_STARTED";

  const advanceJourney = async () => {
    setIsAdvancing(true);
    try {
      await fetch(`${API_BASE_URL}/journey/advance`, { method: "POST" });
      mutate(`${API_BASE_URL}/journey/state`);
    } catch (error) {
      console.error("Failed to advance journey", error);
    } finally {
      setIsAdvancing(false);
    }
  };

  const resetJourney = async () => {
    try {
      await fetch(`${API_BASE_URL}/journey/reset`, { method: "POST" });
      mutate(`${API_BASE_URL}/journey/state`);
      setZkpResult(null);
    } catch (error) {
      console.error("Failed to reset journey", error);
    }
  };

  const verifyEligibility = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsVerifying(true);
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
    } finally {
      setIsVerifying(false);
    }
  };

  const electionSteps: TimelineStep[] = [
    { id: "1", label: "Registration", date: "Step 1", status: journeyState === "NOT_STARTED" ? "pending" : (journeyState === "REGISTRATION" ? "current" : "completed") },
    { id: "2", label: "Primary", date: "Step 2", status: ["NOT_STARTED", "REGISTRATION"].includes(journeyState) ? "pending" : (journeyState === "PRIMARY" ? "current" : "completed") },
    { id: "3", label: "General Election", date: "Step 3", status: ["COMPLETED", "GENERAL_ELECTION"].includes(journeyState) ? (journeyState === "GENERAL_ELECTION" ? "current" : "completed") : "pending" },
  ];

  return (
    <main className="min-h-screen bg-background p-4 sm:p-24 flex flex-col items-center overflow-hidden relative">
      {/* Sentient Mesh Background Effect */}
      <div className="absolute inset-0 -z-10 opacity-20 pointer-events-none">
        <motion.div 
          animate={{ scale: [1, 1.1, 1], opacity: [0.3, 0.5, 0.3] }}
          transition={{ duration: 10, repeat: Infinity, ease: "easeInOut" }}
          className="absolute top-0 left-0 w-full h-full bg-[radial-gradient(circle_at_50%_50%,var(--primary-container),transparent_70%)]"
        />
      </div>

      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="w-full max-w-4xl flex flex-col gap-8 sm:gap-12 bg-surface-container-lowest p-6 sm:p-12 rounded-3xl shadow-ambient border border-outline-variant/30"
      >
        <header className="text-center">
          <motion.div
            initial={{ scale: 0.9 }}
            animate={{ scale: 1 }}
            className="inline-flex items-center gap-2 bg-primary/10 px-4 py-1.5 rounded-full mb-6"
          >
            <ShieldCheck className="w-4 h-4 text-primary" />
            <span className="text-xs font-bold text-primary tracking-wider uppercase">Privacy-First Sentient Mesh</span>
          </motion.div>
          <h1 className="text-[36px] sm:text-[48px] leading-tight font-extrabold text-primary mb-6 tracking-tight">
            Votera <span className="text-secondary">Sentient Guide</span>
          </h1>
          <div className="flex justify-center gap-6 mb-8">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
              <span className="text-[10px] font-bold uppercase tracking-widest text-on-surface-variant">Mesh Status: Optimal</span>
            </div>
            <div className="flex items-center gap-2">
              <ShieldCheck className="w-3 h-3 text-primary" />
              <span className="text-[10px] font-bold uppercase tracking-widest text-on-surface-variant">ZKP Integrity: Verified</span>
            </div>
          </div>
          <p className="text-[18px] sm:text-[20px] leading-relaxed text-on-surface-variant max-w-2xl mx-auto font-medium">
            Navigating the complexities of democracy with factual precision and cryptographic privacy.
          </p>
        </header>

        <section className="bg-surface-container-low p-6 sm:p-10 rounded-2xl border border-surface-variant/50 shadow-inner">
          <Timeline steps={electionSteps} />
          
          <div className="mt-10 flex flex-wrap justify-center gap-4">
             <button 
                id="advance-button"
                aria-label="Advance to the next election step"
                disabled={isAdvancing || journeyState === "COMPLETED"}
                onClick={advanceJourney}
                className="h-[56px] px-8 bg-primary text-on-primary font-bold rounded-xl hover:bg-primary-container hover:text-on-primary-container transition-all shadow-lg active:scale-95 disabled:opacity-50 flex items-center gap-2"
             >
                {isAdvancing ? <RefreshCw className="w-5 h-5 animate-spin" /> : <ArrowRight className="w-5 h-5" />}
                Advance Journey
             </button>
             <button 
                id="reset-button"
                aria-label="Reset the election journey"
                onClick={resetJourney}
                className="h-[56px] px-8 bg-surface-variant text-on-surface-variant font-bold rounded-xl hover:bg-outline-variant transition-all flex items-center gap-2"
             >
                <RefreshCw className="w-5 h-5" />
                Reset
             </button>
          </div>
        </section>

        <section className="bg-surface-container-low p-6 sm:p-10 rounded-2xl border border-surface-variant/50 relative overflow-hidden">
          <div className="flex items-center gap-3 mb-8">
            <div className="w-10 h-10 rounded-lg bg-secondary/10 flex items-center justify-center">
              <ShieldCheck className="w-6 h-6 text-secondary" />
            </div>
            <div>
              <h2 className="text-[22px] font-bold text-primary">ZKP Eligibility Vault</h2>
              <p className="text-xs text-on-surface-variant font-medium uppercase tracking-widest">Zero-Knowledge Verification</p>
            </div>
          </div>

          <form onSubmit={verifyEligibility} className="grid grid-cols-1 sm:grid-cols-12 gap-6 items-end">
            <div className="sm:col-span-4">
              <label htmlFor="age-input" className="block text-sm font-bold text-on-surface mb-2">Voter Age</label>
              <input 
                id="age-input"
                type="number" 
                name="age" 
                required 
                placeholder="18+"
                className="w-full h-[48px] px-4 rounded-xl border-2 border-outline-variant bg-surface-container-lowest text-on-surface focus:outline-none focus:border-primary transition-colors font-medium" 
              />
            </div>
            <div className="sm:col-span-5">
              <label htmlFor="location-input" className="block text-sm font-bold text-on-surface mb-2">Residency Location</label>
              <input 
                id="location-input"
                type="text" 
                name="location" 
                required 
                placeholder="City or Region"
                className="w-full h-[48px] px-4 rounded-xl border-2 border-outline-variant bg-surface-container-lowest text-on-surface focus:outline-none focus:border-primary transition-colors font-medium" 
              />
            </div>
            <div className="sm:col-span-3">
              <button 
                id="verify-button"
                aria-label="Verify your eligibility using ZKP"
                type="submit" 
                disabled={isVerifying}
                className="w-full h-[48px] bg-secondary text-on-secondary font-bold rounded-xl hover:bg-secondary-container hover:text-on-secondary-container transition-all shadow-lg active:scale-95 disabled:opacity-50 flex items-center justify-center gap-2"
              >
                {isVerifying ? <RefreshCw className="w-5 h-5 animate-spin" /> : <Send className="w-4 h-4" />}
                Verify
              </button>
            </div>
          </form>
          
          <AnimatePresence>
            {zkpResult && (
              <motion.div 
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
                exit={{ opacity: 0, height: 0 }}
                className={`mt-8 p-6 rounded-xl border-2 flex gap-4 ${
                  zkpResult.is_eligible 
                    ? 'bg-primary-container/20 border-primary/20 text-on-primary-container' 
                    : 'bg-error-container/20 border-error/20 text-on-error-container'
                }`}
                role="status"
                aria-live="polite"
              >
                <div className="shrink-0 pt-1">
                  {zkpResult.is_eligible ? <CheckCircle2 className="w-6 h-6 text-primary" /> : <AlertCircle className="w-6 h-6 text-error" />}
                </div>
                <div className="flex-1">
                  <p className="font-bold text-[18px] mb-1">{zkpResult.message}</p>
                  {zkpResult.zkp_proof && (
                    <div className="mt-3 bg-surface-container-lowest p-3 rounded-lg border border-outline-variant/30">
                      <p className="text-[10px] uppercase font-black tracking-widest text-on-surface-variant mb-1">Cryptographic Proof Hash</p>
                      <p className="text-[11px] font-mono break-all opacity-80 leading-tight">{zkpResult.zkp_proof}</p>
                    </div>
                  )}
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </section>

        <footer className="text-center pt-4 opacity-50">
          <p className="text-xs font-medium text-on-surface-variant uppercase tracking-[0.2em]">
            Election Guide • Powered by Google Cloud & Vertex AI
          </p>
        </footer>
      </motion.div>
    </main>
  );
}
