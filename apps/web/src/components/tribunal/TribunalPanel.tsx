"use client";

import { useState } from "react";
import { api } from "@/lib/api/client";
import type { TribunalResult } from "@/lib/types";
import { formatReliability, verdictColor } from "@/lib/utils";
import { ClaimDocket } from "./ClaimDocket";

export function TribunalPanel() {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<TribunalResult | null>(null);

  async function runTribunal() {
    if (!question.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const data = await api.askTribunal(question.trim());
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Tribunal failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-6">
      <div className="rounded-lg border border-paper-line bg-ivory p-6 shadow-sm">
        <h2 className="mb-2 text-lg font-semibold">Ask the Tribunal</h2>
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="What does the policy say about external LLM APIs?"
          className="min-h-[100px] w-full rounded-md border border-paper-line bg-white px-3 py-2 text-sm"
          aria-label="Question for the tribunal"
        />
        <button
          type="button"
          disabled={loading || !question.trim()}
          onClick={runTribunal}
          className="mt-3 rounded-md bg-gavel-gold px-4 py-2 text-sm font-medium text-deep-ink disabled:opacity-50"
        >
          {loading ? "Running Tribunal..." : "Run Tribunal"}
        </button>
        {loading && (
          <p className="mt-3 text-sm text-slate-gray">
            The tribunal runs five review stages via the configured LLM. This typically
            takes 30 seconds to 2 minutes.
          </p>
        )}
        {error && (
          <p className="mt-3 text-sm text-overruled-red" role="alert">
            {error}
          </p>
        )}
      </div>

      {result && (
        <>
          <div className="grid gap-4 md:grid-cols-3">
            <div className="rounded-lg border border-paper-line bg-ivory p-4">
              <p className="text-sm text-slate-gray">Tribunal Verdict</p>
              <p
                className={`mt-1 inline-block rounded border px-2 py-1 text-sm font-medium ${verdictColor(result.overall_verdict)}`}
              >
                {result.overall_verdict}
              </p>
            </div>
            <div className="rounded-lg border border-paper-line bg-ivory p-4">
              <p className="text-sm text-slate-gray">Reliability Score</p>
              <p className="mt-1 text-2xl font-semibold text-charcoal">
                {formatReliability(result.reliability_score)}
              </p>
            </div>
            <div className="rounded-lg border border-paper-line bg-ivory p-4">
              <p className="text-sm text-slate-gray">Claims Reviewed</p>
              <p className="mt-1 text-2xl font-semibold">{result.claims.length}</p>
            </div>
          </div>

          <section className="rounded-lg border border-paper-line bg-ivory p-4">
            <h3 className="mb-2 font-semibold">Evidence Locker</h3>
            <div className="space-y-2 text-sm">
              {result.retrieved_sources.map((src) => (
                <div key={src.chunk_id} className="rounded border border-paper-line p-2">
                  <p className="font-medium">
                    {src.filename}
                    {src.page_number ? `, p. ${src.page_number}` : ""}
                  </p>
                  <p className="text-slate-gray">{src.text}</p>
                </div>
              ))}
            </div>
          </section>

          <section className="rounded-lg border border-paper-line bg-ivory p-4">
            <h3 className="mb-2 font-semibold">Witness Answer</h3>
            <p className="text-sm whitespace-pre-wrap">{result.witness_answer.answer_text}</p>
          </section>

          <section className="rounded-lg border border-paper-line bg-ivory p-4">
            <h3 className="mb-2 font-semibold">Prosecutor Objections</h3>
            {result.prosecutor_objections.length === 0 ? (
              <p className="text-sm text-slate-gray">No objections raised.</p>
            ) : (
              <ul className="space-y-2 text-sm">
                {result.prosecutor_objections.map((o) => (
                  <li key={o.objection_id} className="rounded border border-paper-line p-2">
                    <strong>{o.objection_type}:</strong> {o.explanation}
                  </li>
                ))}
              </ul>
            )}
          </section>

          <ClaimDocket
            claims={result.claims}
            verdicts={result.judge_verdict}
            objections={result.prosecutor_objections}
            sources={result.retrieved_sources}
          />

          <section className="rounded-lg border border-paper-line bg-ivory p-4">
            <h3 className="mb-2 font-semibold">Final Ruling</h3>
            <p className="text-sm whitespace-pre-wrap">{result.final_answer}</p>
          </section>
        </>
      )}
    </div>
  );
}
