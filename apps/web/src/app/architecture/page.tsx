export default function ArchitecturePage() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Architecture</h1>

      <section className="rounded-lg border border-paper-line bg-ivory p-6">
        <h2 className="mb-3 text-lg font-semibold">System Overview</h2>
        <pre className="overflow-x-auto rounded bg-parchment p-4 text-xs">
{`User → Next.js Frontend → FastAPI Backend
                              ├── Document Ingestion (extract, chunk, embed)
                              ├── ChromaDB Vector Store
                              ├── Hybrid Retrieval (vector + BM25)
                              └── Tribunal Pipeline
                                    ├── Witness (grounded answer)
                                    ├── Claim Extraction
                                    ├── Prosecutor (objections)
                                    ├── Judge (verdicts)
                                    └── Final Ruling`}
        </pre>
      </section>

      <section className="rounded-lg border border-paper-line bg-ivory p-6">
        <h2 className="mb-3 text-lg font-semibold">Retrieval Pipeline</h2>
        <p className="text-sm text-slate-gray">
          Questions are embedded and matched against document chunks using semantic
          vector search. Hybrid mode combines vector similarity with BM25 keyword
          matching via reciprocal rank fusion for improved recall.
        </p>
      </section>

      <section className="rounded-lg border border-paper-line bg-ivory p-6">
        <h2 className="mb-3 text-lg font-semibold">Agent Workflow</h2>
        <ol className="list-decimal space-y-2 pl-5 text-sm text-slate-gray">
          <li>Witness generates an answer from retrieved evidence only.</li>
          <li>Claims are extracted from the Witness answer.</li>
          <li>Prosecutor challenges each claim against evidence.</li>
          <li>Judge assigns verdicts and confidence scores per claim.</li>
          <li>Final Ruling revises unsupported claims out of the answer.</li>
        </ol>
      </section>

      <section className="rounded-lg border border-paper-line bg-ivory p-6">
        <h2 className="mb-3 text-lg font-semibold">Data Privacy</h2>
        <p className="text-sm text-slate-gray">
          Documents and chunk metadata are stored locally in ChromaDB and SQLite. By
          default, embeddings and tribunal LLM calls use OpenAI. For fully local
          inference, configure Ollama or local embeddings in the API environment—see
          docs/privacy-and-security.md.
        </p>
      </section>

      <section className="rounded-lg border border-paper-line bg-ivory p-6">
        <h2 className="mb-3 text-lg font-semibold">Limitations</h2>
        <ul className="list-disc space-y-2 pl-5 text-sm text-slate-gray">
          <li>Verdict quality depends on LLM capability and prompt adherence.</li>
          <li>Complex PDF layouts may lose structure during extraction.</li>
          <li>Evaluation metrics are heuristic, not ground-truth legal review.</li>
          <li>No reranking model in MVP (stretch goal).</li>
        </ul>
      </section>
    </div>
  );
}
