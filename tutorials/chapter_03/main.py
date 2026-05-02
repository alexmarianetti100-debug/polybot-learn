"""
Chapter 3: Your first scanner.

A polling daemon that fans out across the most-active Polymarket markets,
finds YES/NO pairs whose ask-prices sum to more than $1.02 (theoretical
short-arbitrage opportunities), and prints each one once.

Three pieces:
1. fan-out — fetch event list, then both books per market
2. filter — keep only YES_ask + NO_ask >= THRESHOLD
3. dedupe — bounded-memory deque so the same gap doesn't print every cycle

No auth required. Polymarket's CLOB /book endpoint is public.

Run it:
    pip install -r requirements.txt
    python main.py
"""

import json
import time
from collections import deque

import requests

GAMMA_API = "https://gamma-api.polymarket.com"
CLOB_API = "https://clob.polymarket.com"

THRESHOLD = 1.02         # YES + NO must sum to at least this to flag
SCAN_INTERVAL_SEC = 30
MARKETS_PER_SCAN = 50
SEEN_MAX = 200           # remember this many recent flags before forgetting


def fetch_active_markets(limit: int) -> list[dict]:
    """Fetch the most-active currently-trading markets, flattened."""
    response = requests.get(
        f"{GAMMA_API}/events",
        params={
            "limit": limit,
            "active": "true",
            "closed": "false",
            "order": "volume24hr",
            "ascending": "false",
        },
        timeout=15,
    )
    response.raise_for_status()
    out: list[dict] = []
    for event in response.json():
        for market in event.get("markets", []):
            if not market.get("closed"):
                out.append(market)
    return out


def fetch_book(token_id: str) -> dict | None:
    """Fetch one side of the orderbook. Returns None on any HTTP error.

    We swallow HTTP errors here because a scanner should never crash on
    one bad market — it should log and keep going. Real bots use
    structured logging instead of None-returns; this is the chapter-3
    version of that pattern.
    """
    try:
        response = requests.get(
            f"{CLOB_API}/book",
            params={"token_id": token_id},
            timeout=10,
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None


def best_ask(book: dict | None) -> float | None:
    if not book:
        return None
    asks = book.get("asks", [])
    if not asks:
        return None
    return min(float(a["price"]) for a in asks)


def parse_token_ids(market: dict) -> list[str]:
    """clobTokenIds ships as a JSON-encoded string (same Polymarket quirk
    we hit in chapters 1 and 2)."""
    raw = market.get("clobTokenIds", "[]")
    return json.loads(raw) if isinstance(raw, str) else raw


def scan_once(seen: deque) -> tuple[int, list[str]]:
    """One pass over the active markets. Returns (count_checked, hits)."""
    hits: list[str] = []
    markets = fetch_active_markets(MARKETS_PER_SCAN)
    for market in markets:
        token_ids = parse_token_ids(market)
        if len(token_ids) < 2:
            continue

        yes_ask = best_ask(fetch_book(token_ids[0]))
        no_ask = best_ask(fetch_book(token_ids[1]))
        if yes_ask is None or no_ask is None:
            continue

        total = yes_ask + no_ask
        if total < THRESHOLD:
            continue

        # Dedup key: the pair of token IDs uniquely identifies the market
        # regardless of which side we call YES or NO.
        key = tuple(sorted(token_ids))
        if key in seen:
            continue
        seen.append(key)

        edge_pct = (total - 1.0) * 100
        question = (market.get("question") or "?")[:60]
        hits.append(
            f"  > {question}  YES ${yes_ask:.3f} + NO ${no_ask:.3f} "
            f"= ${total:.3f} ({edge_pct:.1f}% gross)"
        )

    return len(markets), hits


def main() -> None:
    seen: deque = deque(maxlen=SEEN_MAX)
    cycle = 0
    while True:
        cycle += 1
        start = time.time()
        try:
            checked, hits = scan_once(seen)
            elapsed = time.time() - start
            print(f"[scan {cycle}] checked {checked} markets in {elapsed:.1f}s")
            for line in hits:
                print(line)
        except Exception as exc:
            print(f"[scan {cycle}] error: {exc}")
        time.sleep(SCAN_INTERVAL_SEC)


if __name__ == "__main__":
    main()
