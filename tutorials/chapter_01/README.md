# Chapter 1 — Your first market query

A 30-line Python script that fetches active prediction markets from
Polymarket's public Gamma API and prints them with current YES prices.

No signup. No API key. Just an HTTPS GET.

## Run

```bash
pip install -r requirements.txt
python main.py
```

## Expected output

```
2024 Presidential Election
  24h volume: $3,184,202
  - Will Donald Trump win?
    YES @ $0.51
  - Will Kamala Harris win?
    YES @ $0.48
```

The exact markets and prices change minute-by-minute. If you see real
events with real prices, you're done.

## Read the chapter

Full walkthrough at <https://alexmarianetti.com/polybot/chapter-1>.
