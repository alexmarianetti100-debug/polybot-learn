"""
Chapter 4: Sizing with the Kelly criterion.

Compares full / half / quarter Kelly against a fixed-dollar-stake
strategy across 1,000 simulated paths of 200 sequential binary bets.
Reports median final bankroll, 10th-percentile bankroll, worst path,
and max drawdown for each strategy.

No external deps — pure stdlib.

Run it:
    python main.py
"""

import random


def kelly_fraction(p_true: float, price: float) -> float:
    """Optimal fraction of bankroll to bet on YES at given market price.

    Args:
        p_true: your estimated true probability of YES winning (0..1)
        price: market price for YES (0 < price < 1)

    Returns 0 if there is no positive edge (don't bet).
    """
    if price <= 0 or price >= 1:
        return 0.0
    b = (1 - price) / price       # profit per dollar staked
    q = 1 - p_true
    edge = b * p_true - q
    if edge <= 0:
        return 0.0
    return edge / b


def simulate_path(
    fraction: float,
    initial: float = 1000.0,
    p_true: float = 0.55,
    price: float = 0.50,
    n_bets: int = 200,
    seed: int = 0,
) -> list[float]:
    """One bankroll-history path at a constant Kelly multiple."""
    rng = random.Random(seed)
    bankroll = initial
    history = [bankroll]
    b = (1 - price) / price
    for _ in range(n_bets):
        stake = bankroll * fraction
        if rng.random() < p_true:
            bankroll += stake * b   # win: gain b × stake
        else:
            bankroll -= stake       # lose: lose stake
        bankroll = max(bankroll, 0.01)
        history.append(bankroll)
    return history


def fixed_dollar_path(
    stake: float,
    initial: float = 1000.0,
    p_true: float = 0.55,
    price: float = 0.50,
    n_bets: int = 200,
    seed: int = 0,
) -> list[float]:
    """One bankroll-history path at a constant dollar stake (capped at
    current bankroll so we never bet more than we have)."""
    rng = random.Random(seed)
    bankroll = initial
    history = [bankroll]
    b = (1 - price) / price
    for _ in range(n_bets):
        actual_stake = min(stake, bankroll)
        if rng.random() < p_true:
            bankroll += actual_stake * b
        else:
            bankroll -= actual_stake
        bankroll = max(bankroll, 0.01)
        history.append(bankroll)
    return history


def max_drawdown(history: list[float]) -> float:
    """Largest peak-to-trough drop on a bankroll history, as a fraction."""
    peak = history[0]
    worst = 0.0
    for value in history:
        peak = max(peak, value)
        if peak > 0:
            drawdown = (peak - value) / peak
            worst = max(worst, drawdown)
    return worst


def run() -> None:
    p_true = 0.55
    price = 0.50
    n_paths = 1000
    n_bets = 200

    f_star = kelly_fraction(p_true, price)
    print(f"Simulating {n_paths} paths × {n_bets} bets each")
    print(f"Edge: true_p={p_true}, price=${price:.2f} → Kelly fraction = {f_star:.3f}")
    print()

    strategies = [
        ("Full Kelly",     lambda s: simulate_path(f_star,        seed=s)),
        ("Half Kelly",     lambda s: simulate_path(f_star * 0.5,  seed=s)),
        ("Quarter Kelly",  lambda s: simulate_path(f_star * 0.25, seed=s)),
        ("Fixed $20",      lambda s: fixed_dollar_path(20.0,      seed=s)),
    ]

    header = f"  {'Strategy':<15} {'Median':>8}  {'10th-pctile':>11}  {'Worst path':>13}  {'Max drawdown':>13}"
    print(header)
    print(f"  {'─'*15} {'─'*8}  {'─'*11}  {'─'*13}  {'─'*13}")

    for name, run_fn in strategies:
        histories = [run_fn(seed) for seed in range(n_paths)]
        finals = sorted(h[-1] for h in histories)
        median = finals[n_paths // 2]
        p10 = finals[n_paths // 10]
        worst = finals[0]
        max_dd = max(max_drawdown(h) for h in histories)
        print(
            f"  {name:<15} ${median:>6,.0f}  ${p10:>9,.0f}  "
            f"${worst:>11,.0f}  {max_dd:>12.0%}"
        )


if __name__ == "__main__":
    run()
