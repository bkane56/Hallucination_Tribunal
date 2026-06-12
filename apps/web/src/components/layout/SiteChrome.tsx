import Link from "next/link";

const navItems = [
  { href: "/", label: "Home" },
  { href: "/corpus", label: "Corpus" },
  { href: "/tribunal", label: "Tribunal" },
  { href: "/evaluation", label: "Evaluation" },
  { href: "/architecture", label: "Architecture" },
];

export function SiteHeader() {
  return (
    <header className="bg-deep-ink text-ivory border-b border-paper-line">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4">
        <Link href="/" className="text-lg font-semibold tracking-tight">
          The Hallucination Tribunal
        </Link>
        <nav className="flex flex-wrap gap-4 text-sm">
          {navItems.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="text-ivory/80 hover:text-gavel-gold transition-colors"
            >
              {item.label}
            </Link>
          ))}
        </nav>
      </div>
    </header>
  );
}

export function PrivacyBanner() {
  return (
    <div className="border border-paper-line bg-ivory px-4 py-3 text-sm text-slate-gray">
      Privacy note: Documents are stored on the API host. When configured with hosted
      providers (e.g. OpenAI), document chunks and tribunal prompts are sent to third-party
      APIs. Use Ollama or local embeddings for fully private inference.
    </div>
  );
}

export function SiteFooter() {
  return (
    <footer className="mt-auto bg-deep-ink px-4 py-6 text-center text-sm text-ivory/70">
      The Hallucination Tribunal — RAG with adversarial claim verification
    </footer>
  );
}
