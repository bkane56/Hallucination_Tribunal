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
    <header className="border-b border-aged-paper-line bg-deep-ink text-soft-ivory">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <Link href="/" className="text-lg font-semibold tracking-tight">
          The Hallucination Tribunal
        </Link>
        <nav className="flex flex-wrap gap-4 text-sm">
          {navItems.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="text-slate-gray transition-colors hover:text-gavel-gold"
            >
              {item.label}
            </Link>
          ))}
        </nav>
      </div>
    </header>
  );
}
