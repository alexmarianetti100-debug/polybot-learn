import Link from "next/link";

export default function PolybotLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen flex flex-col">
      <header className="border-b border-black/10 dark:border-white/10">
        <div className="mx-auto max-w-3xl px-6 py-4 flex items-center justify-between">
          <Link
            href="/polybot"
            className="font-semibold tracking-tight hover:opacity-70 transition"
          >
            polybot
          </Link>
          <nav className="flex gap-5 text-sm text-[var(--muted)]">
            <Link href="/polybot#chapters" className="hover:text-foreground">
              chapters
            </Link>
            <a
              href="https://github.com/alexmarianetti100-debug/polybot-learn"
              className="hover:text-foreground"
              target="_blank"
              rel="noopener noreferrer"
            >
              github
            </a>
          </nav>
        </div>
      </header>
      <main className="flex-1 mx-auto max-w-3xl w-full px-6 py-12">
        {children}
      </main>
      <footer className="border-t border-black/10 dark:border-white/10 mt-16">
        <div className="mx-auto max-w-3xl px-6 py-6 text-sm text-[var(--muted)] flex flex-wrap gap-4 justify-between">
          <span>
            By{" "}
            <a
              href="https://twitter.com/marianettialex"
              className="underline hover:text-foreground"
            >
              Alex Marianetti
            </a>
            . MIT licensed.
          </span>
          <span>
            <Link href="/polybot" className="hover:text-foreground">
              Home
            </Link>
          </span>
        </div>
      </footer>
    </div>
  );
}
