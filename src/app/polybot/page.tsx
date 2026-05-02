import Link from "next/link";

type ChapterStatus = "available" | "coming-soon";

type Chapter = {
  number: number;
  slug: string;
  title: string;
  blurb: string;
  status: ChapterStatus;
};

const chapters: Chapter[] = [
  {
    number: 0,
    slug: "chapter-0",
    title: "Why prediction markets?",
    blurb:
      "What edges exist, why they're hard to capture, and what you'll build over the next chapters.",
    status: "available",
  },
  {
    number: 1,
    slug: "chapter-1",
    title: "Your first market query",
    blurb:
      "30 lines of Python. Polymarket's public API. No auth. See real prices in your terminal in five minutes.",
    status: "available",
  },
  {
    number: 2,
    slug: "chapter-2",
    title: "Reading an orderbook",
    blurb:
      "The book is more than a price. You'll fetch live bids and asks and compute the bid-ask spread.",
    status: "available",
  },
  {
    number: 3,
    slug: "chapter-3",
    title: "Your first scanner",
    blurb:
      "A daemon that polls hundreds of markets, finds threshold violations, and never trades twice on the same opportunity.",
    status: "available",
  },
  {
    number: 4,
    slug: "chapter-4",
    title: "Sizing with the Kelly criterion",
    blurb:
      "Optimal bet sizing in 20 lines, plus the reason every serious trader uses half-Kelly instead.",
    status: "available",
  },
  {
    number: 5,
    slug: "chapter-5",
    title: "Validation gates",
    blurb:
      "Eight checks every opportunity must pass before you risk a dollar. Most of yours will die at gate 5 or 6.",
    status: "coming-soon",
  },
  {
    number: 6,
    slug: "chapter-6",
    title: "Paper trading",
    blurb:
      "How to simulate fills without lying to yourself. The two fill models that matter and when to use each.",
    status: "coming-soon",
  },
  {
    number: 7,
    slug: "chapter-7",
    title: "Going live (carefully)",
    blurb:
      "Auth, key signing, and the three-layer safety system that makes it structurally impossible to deploy real money by accident.",
    status: "coming-soon",
  },
];

export default function PolybotHome() {
  return (
    <div className="space-y-16">
      <section className="space-y-6">
        <p className="text-sm uppercase tracking-widest text-[var(--accent)]">
          Free curriculum · Open source · Work in progress
        </p>
        <h1 className="text-4xl sm:text-5xl font-semibold tracking-tight leading-tight">
          Build your own prediction-market trading bot.
        </h1>
        <p className="text-lg text-[var(--muted)] max-w-2xl leading-relaxed">
          I&apos;m Alex. I&apos;m 18. I spent eight months building a production
          bot that trades real money on Kalshi and Polymarket. This is the
          curriculum I wish I&apos;d had on day one — written so a beginner can
          clone, run, and ship their own bot.
        </p>
        <div className="flex flex-wrap gap-3 pt-2">
          <Link
            href="/polybot/chapter-0"
            className="inline-flex h-11 items-center rounded-full bg-foreground text-background px-5 text-sm font-medium hover:opacity-90 transition"
          >
            Start with Chapter 0 →
          </Link>
          <a
            href="https://github.com/alexmarianetti/polybot-learn"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex h-11 items-center rounded-full border border-black/15 dark:border-white/15 px-5 text-sm font-medium hover:bg-black/5 dark:hover:bg-white/5 transition"
          >
            View source on GitHub
          </a>
        </div>
      </section>

      <section className="space-y-4">
        <h2 className="text-xl font-semibold tracking-tight">
          What you&apos;ll be able to do
        </h2>
        <ul className="space-y-2 text-[var(--muted)] leading-relaxed">
          <li>
            <span className="text-foreground">→</span> Pull live market data
            from Polymarket and Kalshi without paying for a single API call.
          </li>
          <li>
            <span className="text-foreground">→</span> Detect three classes of
            mispricing: logic arbitrage, short arbitrage, and the
            favorite-longshot bias.
          </li>
          <li>
            <span className="text-foreground">→</span> Size positions with the
            Kelly criterion, run an eight-gate validator, and paper-trade for
            weeks before risking real money.
          </li>
          <li>
            <span className="text-foreground">→</span> Run a small,
            production-shaped bot you actually understand line by line.
          </li>
        </ul>
      </section>

      <section id="chapters" className="space-y-5">
        <h2 className="text-xl font-semibold tracking-tight">Chapters</h2>
        <ol className="space-y-3">
          {chapters.map((c) => {
            const isAvailable = c.status === "available";
            const inner = (
              <>
                <div className="flex items-baseline gap-3">
                  <span className="font-mono text-xs text-[var(--muted)]">
                    {String(c.number).padStart(2, "0")}
                  </span>
                  <span className="font-medium">{c.title}</span>
                  {!isAvailable && (
                    <span className="text-xs text-[var(--muted)] uppercase tracking-wide">
                      coming soon
                    </span>
                  )}
                </div>
                <p className="mt-1 ml-9 text-sm text-[var(--muted)] leading-relaxed">
                  {c.blurb}
                </p>
              </>
            );
            return (
              <li
                key={c.slug}
                className={`rounded-lg border border-black/10 dark:border-white/10 p-4 transition ${
                  isAvailable
                    ? "hover:border-black/30 dark:hover:border-white/30"
                    : "opacity-60"
                }`}
              >
                {isAvailable ? (
                  <Link href={`/polybot/${c.slug}`} className="block">
                    {inner}
                  </Link>
                ) : (
                  <div>{inner}</div>
                )}
              </li>
            );
          })}
        </ol>
      </section>

      <section className="space-y-3 pt-4 border-t border-black/10 dark:border-white/10 pt-8">
        <h2 className="text-xl font-semibold tracking-tight">
          A note on honesty
        </h2>
        <p className="text-[var(--muted)] leading-relaxed">
          This curriculum will not make you rich. Most automated trading
          strategies — including ones I built and tested rigorously — lose
          money. Of the strategies in my own bot: one works, four were killed,
          and the working one took eight months and 17,258 settled markets to
          calibrate. What you&apos;ll learn here is how to build the
          infrastructure honestly, not how to print money.
        </p>
      </section>
    </div>
  );
}
