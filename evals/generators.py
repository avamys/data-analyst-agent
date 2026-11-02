"""Seeded synthetic datasets with planted effects: the right answers are known

Feature names are neutral where they could hint at an effect, so an analysis has
to find the effects in the data rather than assume them from the names.
"""

import numpy as np
import pandas as pd


def _logistic(z: np.ndarray) -> np.ndarray:
    return 1 / (1 + np.exp(-z))


def planted_effects(seed: int) -> pd.DataFrame:
    """Binary target: feat_a strong, feat_b weak, feat_c none, feat_d moderate
    with 15% of its values missing completely at random"""
    rng = np.random.default_rng(seed)
    n = 1000
    a, b, c, d = rng.normal(size=(4, n))
    outcome = rng.random(n) < _logistic(-0.6 + 1.5 * a + 0.3 * b + 0.8 * d)
    d[rng.choice(n, size=150, replace=False)] = np.nan
    return pd.DataFrame(
        {
            "feat_a": a.round(3),
            "feat_b": b.round(3),
            "feat_c": c.round(3),
            "feat_d": d.round(3),
            "outcome": outcome.astype(int),
        }
    )


def pure_noise(seed: int) -> pd.DataFrame:
    """Binary target independent of every feature"""
    rng = np.random.default_rng(seed)
    n = 800
    df = pd.DataFrame(
        rng.normal(size=(n, 5)).round(3), columns=[f"feat_{i}" for i in range(1, 6)]
    )
    df["group"] = rng.choice(["g1", "g2", "g3", "g4"], size=n)
    df["outcome"] = (rng.random(n) < 0.4).astype(int)
    return df


def leakage(seed: int) -> pd.DataFrame:
    """Churn with moderate real predictors, plus refund_issued: an event that
    follows churn and copies the target in 98% of rows"""
    rng = np.random.default_rng(seed)
    n = 1000
    usage = rng.gamma(4, 5, size=n)
    tenure = rng.integers(1, 72, size=n)
    plan = rng.choice(["basic", "plus", "pro"], size=n, p=[0.5, 0.3, 0.2])
    z = (
        -0.9
        - 0.5 * (usage - usage.mean()) / usage.std()
        - 0.4 * (tenure - tenure.mean()) / tenure.std()
        + 0.6 * (plan == "basic")
    )
    churned = (rng.random(n) < _logistic(z)).astype(int)
    flipped = rng.random(n) < 0.02
    return pd.DataFrame(
        {
            "usage_hours": usage.round(1),
            "tenure_months": tenure,
            "plan": plan,
            "refund_issued": np.where(flipped, 1 - churned, churned),
            "churned": churned,
        }
    )


def regression_outliers(seed: int) -> pd.DataFrame:
    """Right-skewed continuous target with 2% extreme outliers: size_sqm strong
    positive, age_years negative, rating none"""
    rng = np.random.default_rng(seed)
    n = 600
    size = rng.uniform(30, 200, size=n)
    age = rng.uniform(0, 60, size=n)
    rating = rng.integers(1, 6, size=n)
    price = np.exp(11 + 0.012 * size - 0.006 * age + rng.normal(0, 0.25, size=n))
    price[rng.choice(n, size=12, replace=False)] *= 8
    return pd.DataFrame(
        {
            "size_sqm": size.round(1),
            "age_years": age.round(1),
            "rating": rating,
            "price": price.round(-2),
        }
    )


def string_target(seed: int) -> pd.DataFrame:
    """Target stored as "yes"/"no": monthly contracts, higher fees and more
    support calls raise churn; region has no effect"""
    rng = np.random.default_rng(seed)
    n = 800
    fee = rng.uniform(20, 120, size=n)
    calls = rng.poisson(1.5, size=n)
    contract = rng.choice(["monthly", "annual"], size=n, p=[0.6, 0.4])
    region = rng.choice(["north", "south", "east", "west"], size=n)
    z = -2.2 + 0.02 * (fee - 70) + 0.45 * calls + 1.0 * (contract == "monthly")
    churned = rng.random(n) < _logistic(z)
    return pd.DataFrame(
        {
            "monthly_fee": fee.round(2),
            "support_calls": calls,
            "contract": contract,
            "region": region,
            "churned_flag": np.where(churned, "yes", "no"),
        }
    )


def datetime_trend(seed: int) -> pd.DataFrame:
    """Two years of daily sales: upward trend, higher on weekends and promotion
    days; temperature follows the seasons but doesn't affect sales"""
    rng = np.random.default_rng(seed)
    dates = pd.date_range("2023-01-01", periods=730, freq="D")
    t = np.arange(len(dates))
    weekend = dates.dayofweek >= 5
    promo = rng.random(len(dates)) < 0.15
    sales = 200 + 0.15 * t + 40 * weekend + 30 * promo + rng.normal(0, 15, len(dates))
    temperature = (
        12 + 9 * np.sin(2 * np.pi * (t - 100) / 365) + rng.normal(0, 3, len(dates))
    )
    return pd.DataFrame(
        {
            "date": dates.strftime("%Y-%m-%d"),
            "temperature": temperature.round(1),
            "promo": promo.astype(int),
            "sales": sales.round(1),
        }
    )


GENERATORS = {
    "planted_effects": planted_effects,
    "pure_noise": pure_noise,
    "leakage": leakage,
    "regression_outliers": regression_outliers,
    "string_target": string_target,
    "datetime_trend": datetime_trend,
}
