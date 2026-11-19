"""Held-out cases: seeded synthetic datasets with planted answers

Generator names carry an ho_ prefix so they never clash with evals/generators.py.
The values the case files state as facts (shares, group rates, counts) are fixed
by construction and hold for any seed; only the effects are random draws.
"""

import numpy as np
import pandas as pd

from evals.generators import _logistic


def _shuffled(df: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    return df.iloc[rng.permutation(len(df))].reset_index(drop=True)


def ho_visits(seed: int) -> pd.DataFrame:
    """Binary target. The tier mix moves from bronze to gold over eight quarters
    (gold 8% -> 64% of visits) and gold returns far more often. Within every tier
    the repeat rate falls, so the pooled rate rises only because of the mix"""
    rng = np.random.default_rng(seed)
    quarter, tier = [], []
    for q in range(1, 9):
        counts = {"bronze": 180 - 20 * (q - 1), "silver": 50, "gold": 20 + 20 * (q - 1)}
        for t, k in counts.items():
            quarter += [q] * k
            tier += [t] * k
    quarter, tier = np.array(quarter), np.array(tier)
    n = len(quarter)
    base = np.select([tier == "bronze", tier == "silver"], [-2.0, 0.5], default=3.5)
    repeat = rng.random(n) < _logistic(base - 0.25 * (quarter - 1))
    df = pd.DataFrame(
        {
            "quarter": quarter,
            "tier": tier,
            "age": rng.normal(41, 12, n).clip(18, 85).round().astype(int),
            "distance_km": rng.gamma(2, 6, n).round(1),
            "staff_on_shift": rng.integers(3, 13, n),
            "repeat_visit": repeat.astype(int),
        }
    )
    return _shuffled(df, rng)


def ho_accounts(seed: int) -> pd.DataFrame:
    """Binary target. Renewal is exactly 80/65/50/35% at 0/10/20/30% discount;
    within each level the renewers are the accounts highest on a score driven up
    by support_tickets and log seats. contract_months, region and signup_month
    have no effect"""
    rng = np.random.default_rng(seed)
    renewals = {0: 320, 10: 260, 20: 200, 30: 140}  # of 400 accounts per level
    discount = np.repeat(list(renewals), 400)
    n = len(discount)
    tickets = rng.poisson(3.0, n)
    seats = np.maximum(1, rng.lognormal(2.3, 0.9, n).round()).astype(int)
    log_seats = np.log(seats)
    score = (
        0.7 * (tickets - tickets.mean()) / tickets.std()
        + 0.6 * (log_seats - log_seats.mean()) / log_seats.std()
        + rng.normal(size=n)
    )
    renewed = np.zeros(n, dtype=int)
    for level, k in renewals.items():
        idx = np.flatnonzero(discount == level)
        renewed[idx[np.argsort(-score[idx], kind="stable")[:k]]] = 1
    df = pd.DataFrame(
        {
            "discount_pct": discount,
            "seats": seats,
            "support_tickets": tickets,
            "contract_months": rng.choice([12, 24], n),
            "region": rng.choice(["north", "south", "east", "west"], n),
            "signup_month": rng.integers(1, 13, n),
            "renewed": renewed,
        }
    )
    return _shuffled(df, rng)


def ho_shipments(seed: int) -> pd.DataFrame:
    """Numeric target. 150 of 1000 weights are stored as 0.0 (missing; real
    weights are >= 0.2 kg) and those parcels take ~30 h longer. Among recorded
    weights: +1.5 h per kg, +0.05 h per km. depot, items, weekday: no effect"""
    rng = np.random.default_rng(seed)
    n = 1000
    weight = rng.lognormal(1.455, 0.5545, n).clip(0.2, None)  # mean ~5 kg
    distance = rng.uniform(5, 300, n)
    missing = np.zeros(n, dtype=bool)
    missing[rng.choice(n, size=150, replace=False)] = True
    hours = 20 + 1.5 * weight + 0.05 * distance + 30 * missing + rng.normal(0, 4, n)
    df = pd.DataFrame(
        {
            "parcel_weight_kg": np.where(missing, 0.0, weight.round(2)),
            "distance_km": distance.round(1),
            "depot": rng.choice(["alpha", "beta", "gamma", "delta"], n),
            "items": rng.integers(1, 11, n),
            "weekday": rng.choice(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], n),
            "delivery_hours": hours.round(1),
        }
    )
    return _shuffled(df, rng)


def ho_students(seed: int) -> pd.DataFrame:
    """Numeric target (score_gain = post - pre). The 250 lowest pre-scorers get
    extra_sessions, which do nothing: their gain is regression to the mean.
    attendance_pct raises the gain; age and class_size have no effect"""
    rng = np.random.default_rng(seed)
    n = 1000
    ability = rng.normal(60, 10, n)
    attendance = rng.uniform(50, 100, n).round(1)
    pre = (ability + rng.normal(0, 8, n)).round(1)
    post = ability + 0.2 * (attendance - 75) + rng.normal(0, 8, n)
    extra = np.zeros(n, dtype=int)
    extra[np.argsort(pre, kind="stable")[:250]] = 1
    df = pd.DataFrame(
        {
            "pre_score": pre,
            "extra_sessions": extra,
            "attendance_pct": attendance,
            "age": rng.integers(15, 19, n),
            "class_size": rng.integers(18, 33, n),
            "score_gain": (post - pre).round(1),
        }
    )
    return _shuffled(df, rng)


GENERATORS = {
    "ho_visits": ho_visits,
    "ho_accounts": ho_accounts,
    "ho_shipments": ho_shipments,
    "ho_students": ho_students,
}