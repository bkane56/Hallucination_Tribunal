import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";
import type { Verdict } from "@/lib/types";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function verdictColor(verdict: Verdict | string): string {
  switch (verdict) {
    case "Supported":
      return "text-verdict-teal bg-verdict-teal/10 border-verdict-teal/30";
    case "Partially Supported":
      return "text-objection-amber bg-objection-amber/10 border-objection-amber/30";
    case "Not Enough Evidence":
      return "text-slate-gray bg-slate-gray/10 border-slate-gray/30";
    case "Unsupported":
      return "text-overruled-red bg-overruled-red/10 border-overruled-red/30";
    case "Contradicted":
      return "text-dark-red bg-dark-red/10 border-dark-red/30";
    default:
      return "text-charcoal bg-ivory border-paper-line";
  }
}

export function formatReliability(score: number | string): string {
  if (score === "Not Applicable") return score;
  if (typeof score === "number") return `${Math.round(score * 100)}%`;
  return String(score);
}
