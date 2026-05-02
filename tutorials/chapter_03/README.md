# Chapter 3 — Your first scanner

A polling daemon that finds short-arbitrage opportunities on Polymarket
by checking whether `YES_ask + NO_ask` exceeds a threshold.

## Run it

```bash
pip install -r requirements.txt
python main.py
```

The scanner runs forever. Stop with `Ctrl+C`. Most cycles will print
nothing — that's correct. Real opportunities at >2% gross are rare and
short-lived.

## What this teaches

- The three-job structure of any scanner: **fan-out → filter → dedupe**
- Bounded-memory dedup with `collections.deque(maxlen=N)`
- The honest distinction between `gross` and `net` edge
- Why sync `requests` is fine until it isn't

## Tunable knobs

- `THRESHOLD` — minimum `YES+NO` total to flag. Lower for noise testing,
  higher for production-shaped triggers.
- `SCAN_INTERVAL_SEC` — how often to poll. Don't go below 10s without
  reading Polymarket's rate-limit docs.
- `MARKETS_PER_SCAN` — how many markets to check per cycle. The scan
  takes ~`MARKETS_PER_SCAN * 2 * 100ms` because it's sequential.

## Try this before chapter 4

1. Lower `THRESHOLD` to `1.005` and observe how much noise appears.
2. Add a timestamp column to each hit and run for an hour. Do gaps
   cluster around any time of day?
