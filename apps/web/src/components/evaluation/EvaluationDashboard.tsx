"use client";

import { useCallback, useEffect, useState } from "react";
import { api } from "@/lib/api/client";
import type { EvaluationRun } from "@/lib/types";
import { formatReliability } from "@/lib/utils";

export function EvaluationDashboard() {
  const [loading, setLoading] = useState(false);
  const [historyLoading, setHistoryLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [run, setRun] = useState<EvaluationRun | null>(null);
  const [history, setHistory] = useState<EvaluationRun[]>([]);

  const loadHistory = useCallback(async () => {
    setHistoryLoading(true);
    try {
      const result = await api.listEvaluationRuns();
      setHistory(result.runs);
    } catch {
      setHistory([]);
    } finally {
      setHistoryLoading(false);
    }
  }, []);

  useEffect(() => {
    void loadHistory();
  }, [loadHistory]);

  async function handleRunAll() {
    setLoading(true);
    setError(null);
    try {
      const result = await api.runEvaluations();
      setRun(result);
      await loadHistory();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Evaluation failed");
    } finally {
      setLoading(false);
    }
  }

  async function handleSelectRun(runId: string) {
    setError(null);
    try {
      const selected = await api.getEvaluationRun(runId);
      setRun(selected);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load run");
    }
  }

  const metrics = run?.aggregate_metrics as Record<string, number> | undefined;

  return (
    <div className="space-y-6">
      <div className="rounded-lg border border-paper-line bg-ivory p-6 shadow-sm">
        <h2 className="mb-2 text-lg font-semibold">Evaluation Dashboard</h2>
        <p className="mb-4 text-sm text-slate-gray">
          Run predefined test questions against the tribunal pipeline and review quality
          metrics.
        </p>
        <button
          type="button"
          disabled={loading}
          onClick={handleRunAll}
          className="rounded-md bg-gavel-gold px-4 py-2 text-sm font-medium text-deep-ink disabled:opacity-50"
        >
          {loading ? "Running Evaluations..." : "Run All Evaluations"}
        </button>
        {error && (
          <p className="mt-3 text-sm text-overruled-red" role="alert">
            {error}
          </p>
        )}
      </div>

      {!historyLoading && history.length > 0 && (
        <div className="rounded-lg border border-paper-line bg-ivory p-4">
          <h3 className="mb-3 font-semibold">Run History</h3>
          <ul className="space-y-2 text-sm">
            {history.map((item) => {
              const passRate = item.aggregate_metrics?.pass_rate;
              const label =
                typeof passRate === "number"
                  ? `${Math.round(passRate * 100)}% pass`
                  : "completed";
              return (
                <li key={item.run_id}>
                  <button
                    type="button"
                    onClick={() => handleSelectRun(item.run_id)}
                    className="text-left text-charcoal underline-offset-2 hover:underline"
                  >
                    {new Date(item.completed_at).toLocaleString()} — {label}
                  </button>
                </li>
              );
            })}
          </ul>
        </div>
      )}

      {run && metrics && (
        <>
          <div className="grid gap-4 md:grid-cols-4">
            <MetricCard label="Pass Rate" value={`${Math.round((metrics.pass_rate ?? 0) * 100)}%`} />
            <MetricCard
              label="Retrieval Hit Rate"
              value={`${Math.round((metrics.retrieval_hit_rate ?? 0) * 100)}%`}
            />
            <MetricCard
              label="Avg Citation Accuracy"
              value={`${Math.round((metrics.avg_citation_accuracy ?? 0) * 100)}%`}
            />
            <MetricCard
              label="Unsupported Claims"
              value={String(metrics.total_unsupported_claims ?? 0)}
            />
          </div>

          <div className="rounded-lg border border-paper-line bg-ivory p-4">
            <h3 className="mb-3 font-semibold">Case File Results</h3>
            <div className="overflow-x-auto">
              <table className="min-w-full text-left text-sm">
                <thead>
                  <tr className="border-b border-paper-line text-slate-gray">
                    <th className="px-2 py-2">Question</th>
                    <th className="px-2 py-2">Retrieval Hit</th>
                    <th className="px-2 py-2">Reliability</th>
                    <th className="px-2 py-2">Unsupported</th>
                    <th className="px-2 py-2">Passed</th>
                  </tr>
                </thead>
                <tbody>
                  {run.case_results.map((c) => (
                    <tr key={c.case_id} className="border-b border-paper-line/60">
                      <td className="px-2 py-2 max-w-md">{c.question}</td>
                      <td className="px-2 py-2">{c.retrieval_hit ? "Yes" : "No"}</td>
                      <td className="px-2 py-2">{formatReliability(c.reliability_score)}</td>
                      <td className="px-2 py-2">{c.unsupported_claim_count}</td>
                      <td className="px-2 py-2">{c.passed ? "Pass" : "Fail"}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}
    </div>
  );
}

function MetricCard({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg border border-paper-line bg-ivory p-4 shadow-sm">
      <p className="text-sm text-slate-gray">{label}</p>
      <p className="mt-1 text-2xl font-semibold text-charcoal">{value}</p>
    </div>
  );
}
