"""
Chapter 2: Reading an orderbook.

Fetches a live orderbook from Polymarket's public CLOB API, then prints
the best bid, best ask, midpoint, spread, and top-of-book depth.

No auth required. The /book endpoint is public, just like /events.

Run it:
    pip install -r requirements.txt
    python main.py
"""

import json
import requests

GAMMA_API = "https://gamma-api.polymarket.com"
CLOB_API = "https://clob.polymarket.com"


def fetch_top_market() -> dict:
    """Pick the most-active currently-trading market."""
    response = requests.get(
        f"{GAMMA_API}/events",
        params={
            "limit": 1,
            "active": "true",
            "closed": "false",
            "order": "volume24hr",
            "ascending": "false",
        },
        timeout=10,
    )
    response.raise_for_status()
    for event in response.json():
        for market in event.get("markets", []):
            if not market.get("closed"):
                return market
    raise RuntimeError("No active markets found")


def fetch_orderbook(token_id: str) -> dict:
    """Fetch one side of the orderbook by token ID.

    Each Polymarket binary market has two tokens — one for YES, one for
    NO — and each token has its own independent orderbook.
    """
    response = requests.get(
        f"{CLOB_API}/book",
        params={"token_id": token_id},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def main() -> None:
    market = fetch_top_market()
    print(f"Market: {market.get('question', '?')}\n")

    # clobTokenIds ships as a JSON-encoded string (same Polymarket quirk
    # we hit with outcomePrices in chapter 1).
    token_ids_raw = market.get("clobTokenIds", "[]")
    token_ids = (
        json.loads(token_ids_raw)
        if isinstance(token_ids_raw, str)
        else token_ids_raw
    )
    if not token_ids:
        print("No CLOB token IDs — market not yet live on the orderbook.")
        return

    yes_token = token_ids[0]  # outcome 0 = YES
    book = fetch_orderbook(yes_token)

    bids = book.get("bids", [])
    asks = book.get("asks", [])

    if not bids or not asks:
        print("Empty book — illiquid market. Try a different one.")
        return

    # Defensive: don't assume the API sorts these for us. The "best" bid
    # is the highest price someone is willing to BUY at; the "best" ask
    # is the lowest price someone is willing to SELL at.
    best_bid = max(float(b["price"]) for b in bids)
    best_ask = min(float(a["price"]) for a in asks)

    mid = (best_bid + best_ask) / 2
    spread = best_ask - best_bid

    print(f"Best bid: ${best_bid:.3f}")
    print(f"Best ask: ${best_ask:.3f}")
    print(f"Mid:      ${mid:.3f}")
    print(f"Spread:   ${spread:.3f} ({spread / mid * 100:.1f}%)")

    # How many contracts can you trade at the best price before slipping
    # to the next level? That's the top-of-book depth.
    bid_size = sum(float(b["size"]) for b in bids if float(b["price"]) == best_bid)
    ask_size = sum(float(a["size"]) for a in asks if float(a["price"]) == best_ask)

    print(f"\nDepth at top level:")
    print(f"  Bid: {bid_size:,.0f} contracts")
    print(f"  Ask: {ask_size:,.0f} contracts")


if __name__ == "__main__":
    main()
