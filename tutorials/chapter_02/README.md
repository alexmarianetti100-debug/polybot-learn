# Chapter 2 — Reading an orderbook

Fetches a live orderbook from Polymarket's public CLOB API and computes
the best bid, best ask, midpoint, spread, and top-of-book depth.

## Run

```bash
pip install -r requirements.txt
python main.py
```

## Expected output

```
Market: Will the Fed cut rates in December?

Best bid: $0.420
Best ask: $0.435
Mid:      $0.428
Spread:   $0.015 (3.5%)

Depth at top level:
  Bid: 1,250 contracts
  Ask: 4,800 contracts
```

The exact market and prices change minute-by-minute.

## Read the chapter

Full walkthrough at <https://alexmarianetti.com/polybot/chapter-2>.
