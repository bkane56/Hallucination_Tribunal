export function SiteFooter() {
  return (
    <footer className="mt-auto border-t border-aged-paper-line bg-deep-ink px-6 py-6 text-sm text-slate-gray">
      <div className="mx-auto flex max-w-6xl flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
        <p>Local-first RAG with adversarial claim review.</p>
        <p>Documents stay on your machine unless you opt into a hosted LLM.</p>
      </div>
    </footer>
  );
}
