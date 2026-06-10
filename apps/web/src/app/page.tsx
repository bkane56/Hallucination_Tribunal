import Link from "next/link";

export default function HomePage() {
  return (
    <div className="space-y-8">
      <section className="rounded-lg border border-paper-line bg-ivory p-8 shadow-sm">
        <h1 className="text-3xl font-bold text-charcoal">
          The Hallucination Tribunal
        </h1>
        <p className="mt-4 max-w-3xl text-lg text-slate-gray">
          A RAG-powered courtroom for AI answers. The Witness generates grounded
          responses, the Prosecutor challenges claims, and the Judge delivers a
          transparent verdict with citations.
        </p>
        <div className="mt-6 flex flex-wrap gap-3">
          <Link
            href="/corpus"
            className="rounded-md bg-gavel-gold px-4 py-2 text-sm font-medium text-deep-ink"
          >
            Upload Documents
          </Link>
          <Link
            href="/tribunal"
            className="rounded-md border border-paper-line px-4 py-2 text-sm font-medium hover:bg-parchment"
          >
            Ask the Tribunal
          </Link>
          <Link
            href="/evaluation"
            className="rounded-md border border-paper-line px-4 py-2 text-sm font-medium hover:bg-parchment"
          >
            Evaluation Dashboard
          </Link>
        </div>
      </section>

      <section className="grid gap-4 md:grid-cols-3">
        <div className="rounded-lg border border-paper-line bg-ivory p-4">
          <h2 className="font-semibold">Why it matters</h2>
          <p className="mt-2 text-sm text-slate-gray">
            Enterprise teams need answers they can trust. Claim-level verification
            catches hallucinations before they reach users.
          </p>
        </div>
        <div className="rounded-lg border border-paper-line bg-ivory p-4">
          <h2 className="font-semibold">Architecture</h2>
          <p className="mt-2 text-sm text-slate-gray">
            Hybrid retrieval, structured agent pipeline, local-first privacy with
            optional hosted LLM providers.
          </p>
        </div>
        <div className="rounded-lg border border-paper-line bg-ivory p-4">
          <h2 className="font-semibold">Courtroom metaphor</h2>
          <p className="mt-2 text-sm text-slate-gray">
            Witness, Prosecutor, and Judge roles make AI verification explainable
            to hiring managers and compliance teams.
          </p>
        </div>
      </section>
    </div>
  );
}
