# Chapter 4 — Sizing with the Kelly criterion

A Monte Carlo simulation comparing full / half / quarter Kelly against
fixed-dollar sizing across 1,000 paths of 200 sequential bets.

## Run it

```bash
python main.py
```

No `pip install` step — pure stdlib. Output is deterministic across
runs (seeded paths) so you can A/B test parameter changes confidently.

## What this teaches

- The Kelly fraction in three lines of math
- Why full Kelly is theoretically optimal but practically suicidal
- Why half-Kelly is the production default
- How sizing rules compound (or don't) over long horizons

## Try this

1. Set `p_true = 0.51`. Watch the median collapse — small edges punish
   sizing mistakes brutally.
2. Set `p_true` to one value but compute Kelly with a different value
   (simulate your edge being mis-estimated). Watch full-Kelly break.
3. Bump `n_bets` to `5000`. Half-Kelly often catches full-Kelly because
   the drawdown protection keeps it from any single ruinous streak.
