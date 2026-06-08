import Link from "next/link";

import { Button } from "@/components/ui/button";
import { fetchHealth } from "@/lib/api/health";

export default async function Home() {
  let apiStatus = "unavailable";

  try {
    const health = await fetchHealth();
    apiStatus = `${health.status} (v${health.version})`;
  } catch {
    apiStatus = "unavailable — start the API with uv run uvicorn";
  }

  return (
    <div className="mx-auto max-w-6xl px-6 py-16">
      <section className="rounded-xl border border-aged-paper-line bg-soft-ivory p-10 shadow-sm">
        <p className="text-sm font-medium uppercase tracking-widest text-verdict-teal">
          Portfolio RAG Application
        </p>
        <h1 className="mt-4 max-w-3xl text-4xl font-semibold tracking-tight text-charcoal">
          Every AI answer gets its day in court.
        </h1>
        <p className="mt-6 max-w-2xl text-lg leading-8 text-slate-gray">
          The Hallucination Tribunal retrieves evidence from your document
          corpus, generates a grounded Witness Answer, then subjects each claim
          to Prosecutor objections and a Judge&apos;s Verdict before issuing a
          Final Ruling.
        </p>

        <div className="mt-8 flex flex-wrap gap-4">
          <Link href="/corpus">
            <Button>Upload Evidence</Button>
          </Link>
          <Link href="/tribunal">
            <Button variant="secondary">Run Tribunal</Button>
          </Link>
          <Link href="/architecture">
            <Button variant="ghost">View Architecture</Button>
          </Link>
        </div>
      </section>

      <section className="mt-10 grid gap-6 md:grid-cols-3">
        {[
          {
            title: "Witness",
            body: "Generates answers strictly from retrieved Evidence Locker chunks with citations.",
          },
          {
            title: "Prosecutor",
            body: "Extracts claims and files objections when evidence is missing or contradicted.",
          },
          {
            title: "Judge",
            body: "Assigns per-claim verdicts and produces a reliability-scored Final Ruling.",
          },
        ].map((role) => (
          <article
            key={role.title}
            className="rounded-lg border border-aged-paper-line bg-soft-ivory p-6"
          >
            <h2 className="text-lg font-semibold text-charcoal">{role.title}</h2>
            <p className="mt-3 text-sm leading-6 text-slate-gray">{role.body}</p>
          </article>
        ))}
      </section>

      <p className="mt-10 text-sm text-slate-gray">
        API status: <span className="font-medium text-charcoal">{apiStatus}</span>
      </p>
    </div>
  );
}
