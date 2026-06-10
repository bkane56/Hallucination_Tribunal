"use client";

import { Fragment, useMemo, useState } from "react";
import type {
  Claim,
  JudgeVerdict,
  ProsecutorObjection,
  RetrievedSource,
  Verdict,
} from "@/lib/types";
import { cn, verdictColor } from "@/lib/utils";

type SortKey = "verdict" | "confidence";

interface ClaimDocketProps {
  claims: Claim[];
  verdicts: JudgeVerdict[];
  objections: ProsecutorObjection[];
  sources: RetrievedSource[];
}

export function ClaimDocket({ claims, verdicts, objections, sources }: ClaimDocketProps) {
  const [sortKey, setSortKey] = useState<SortKey>("confidence");
  const [expanded, setExpanded] = useState<string | null>(null);

  const rows = useMemo(() => {
    return claims.map((claim) => {
      const verdict = verdicts.find((v) => v.claim_id === claim.claim_id);
      const objection = objections.find((o) => o.claim_id === claim.claim_id);
      const evidence = sources
        .filter((s) => verdict?.supporting_sources.includes(s.filename))
        .slice(0, 2);
      return { claim, verdict, objection, evidence };
    });
  }, [claims, verdicts, objections, sources]);

  const sorted = useMemo(() => {
    const copy = [...rows];
    copy.sort((a, b) => {
      if (sortKey === "confidence") {
        return (b.verdict?.confidence ?? 0) - (a.verdict?.confidence ?? 0);
      }
      return (a.verdict?.verdict ?? "").localeCompare(b.verdict?.verdict ?? "");
    });
    return copy;
  }, [rows, sortKey]);

  if (claims.length === 0) {
    return (
      <div className="rounded-lg border border-paper-line bg-ivory p-4 text-sm text-slate-gray">
        No factual claims extracted for review.
      </div>
    );
  }

  return (
    <div className="rounded-lg border border-paper-line bg-ivory p-4 shadow-sm">
      <div className="mb-4 flex items-center justify-between">
        <h3 className="text-lg font-semibold">Claim Docket</h3>
        <div className="flex gap-2 text-sm">
          <button
            type="button"
            className={cn("rounded px-2 py-1", sortKey === "verdict" && "bg-parchment")}
            onClick={() => setSortKey("verdict")}
          >
            Sort by Verdict
          </button>
          <button
            type="button"
            className={cn("rounded px-2 py-1", sortKey === "confidence" && "bg-parchment")}
            onClick={() => setSortKey("confidence")}
          >
            Sort by Confidence
          </button>
        </div>
      </div>
      <div className="overflow-x-auto">
        <table className="min-w-full text-left text-sm">
          <thead>
            <tr className="border-b border-paper-line text-slate-gray">
              <th className="px-2 py-2">Claim</th>
              <th className="px-2 py-2">Verdict</th>
              <th className="px-2 py-2">Confidence</th>
              <th className="px-2 py-2">Evidence</th>
              <th className="px-2 py-2">Prosecutor Objection</th>
              <th className="px-2 py-2">Judge&apos;s Reasoning</th>
              <th className="px-2 py-2">Recommended Revision</th>
            </tr>
          </thead>
          <tbody>
            {sorted.map(({ claim, verdict, objection, evidence }) => (
              <Fragment key={claim.claim_id}>
                <tr
                  className="border-b border-paper-line/60 cursor-pointer hover:bg-parchment/50"
                  onClick={() =>
                    setExpanded(expanded === claim.claim_id ? null : claim.claim_id)
                  }
                >
                  <td className="px-2 py-2 max-w-xs">{claim.claim_text}</td>
                  <td className="px-2 py-2">
                    <span
                      className={cn(
                        "inline-block rounded border px-2 py-0.5 text-xs font-medium",
                        verdictColor((verdict?.verdict ?? "Not Enough Evidence") as Verdict)
                      )}
                    >
                      {verdict?.verdict ?? "Pending"}
                    </span>
                  </td>
                  <td className="px-2 py-2">
                    {verdict ? verdict.confidence.toFixed(2) : "—"}
                  </td>
                  <td className="px-2 py-2 max-w-xs">
                    {evidence.map((e) => e.filename).join(", ") || "—"}
                  </td>
                  <td className="px-2 py-2 max-w-xs">
                    {objection?.explanation ?? "—"}
                  </td>
                  <td className="px-2 py-2 max-w-xs">{verdict?.explanation ?? "—"}</td>
                  <td className="px-2 py-2 max-w-xs">
                    {verdict?.recommended_revision ?? "—"}
                  </td>
                </tr>
                {expanded === claim.claim_id && (
                  <tr className="bg-parchment/40">
                    <td colSpan={7} className="px-4 py-3 text-sm">
                      <p>
                        <strong>Original sentence:</strong>{" "}
                        {claim.extracted_from_sentence || claim.claim_text}
                      </p>
                      {evidence.map((e) => (
                        <p key={e.chunk_id} className="mt-2">
                          <strong>Evidence:</strong> [{e.filename}
                          {e.page_number ? `, p. ${e.page_number}` : ""}] {e.text}
                        </p>
                      ))}
                      {objection && (
                        <p className="mt-2">
                          <strong>Prosecutor objection:</strong> {objection.explanation}
                        </p>
                      )}
                      {verdict && (
                        <p className="mt-2">
                          <strong>Judge reasoning:</strong> {verdict.explanation}
                        </p>
                      )}
                    </td>
                  </tr>
                )}
              </Fragment>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
