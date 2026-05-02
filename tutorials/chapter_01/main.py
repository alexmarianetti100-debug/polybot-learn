"""
Chapter 1: Your first prediction-market query.

This script fetches the top active markets from Polymarket and prints
the question and current YES price for each.

Polymarket's "Gamma" API is a public REST endpoint — no signup, no API
key, just an HTTP GET. That's why we picked it for chapter 1.

Run it:
    pip install -r requirements.txt
    python main.py
"""

import json
import requests

# Polymarket's public REST API. No auth required for read endpoints.
GAMMA_API = "https://gamma-api.polymarket.com"


def fetch_top_events(limit: int = 5) -> list[dict]:
    """Return the top `limit` active events sorted by 24-hour volume.

    The /events endpoint returns a flat list of events; each event
    contains one or more individual markets (the YES/NO contracts you
    can actually trade).
    """
    response = requests.get(
        f"{GAMMA_API}/events",
        params={
            "limit": limit,
            "active": "true",
            "closed": "false",
            "order": "volume24hr",
            "ascending": "false",
        },
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def main() -> None:
    events = fetch_top_events(limit=3)

    for event in events:
        title = event.get("title", "(untitled)")
        volume = float(event.get("volume24hr", 0) or 0)
        print(f"\n{title}")
        print(f"  24h volume: ${volume:,.0f}")

        for market in event.get("markets", []):
            if market.get("closed"):
                continue
            question = market.get("question", "(no question)")[:80]

            # outcomePrices ships as a JSON-encoded *string*, not a list.
            # That's a Polymarket quirk — we parse it back into a list.
            prices_raw = market.get("outcomePrices", "[]")
            prices = (
                json.loads(prices_raw)
                if isinstance(prices_raw, str)
                else prices_raw
            )
            yes_price = prices[0] if prices else "?"

            print(f"  - {question}")
            print(f"    YES @ ${yes_price}")


if __name__ == "__main__":
    main()
