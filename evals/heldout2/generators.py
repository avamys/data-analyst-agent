"""Held-out cases, batch 2: seeded synthetic datasets with planted answers

Generator names carry an h5_ prefix so they never clash with evals/generators.py
or evals/heldout/generators.py. The counts the case file states as facts are
fixed by construction and hold for any seed; only the effects are random draws.
"""

import numpy as np
import pandas as pd


def _shuffled(df: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    return df.iloc[rng.permutation(len(df))].reset_index(drop=True)


def h5_hotel_stays(seed: int) -> pd.DataFrame:
    """Numeric target (stay_rating, 1-10). 125 of 900 ratings are stored as 99
    (guest gave no rating): 16 of 320 direct, 22 of 310 website and 87 of 270
    agency bookings. Among rated stays: agency -1.1 and website -0.2 vs direct;
    superior +0.4 and suite +1.1 vs standard. nights, guests, lead_time_days:
    no effect; nightly_rate_eur follows room type"""
    rng = np.random.default_rng(seed)
    channels = {"direct": (320, 16), "website": (310, 22), "agency": (270, 87)}
    channel = np.repeat(list(channels), [k for k, _ in channels.values()])
    n = len(channel)
    room = rng.choice(["standard", "superior", "suite"], n, p=[0.50, 0.35, 0.15])
    latent = (
        7.0
        + np.select([channel == "website", channel == "agency"], [-0.2, -1.1], default=0.0)
        + np.select([room == "superior", room == "suite"], [0.4, 1.1], default=0.0)
        + rng.normal(0, 1.4, n)
    )
    rating = np.clip(np.rint(latent), 1, 10).astype(int)
    for ch, (_, unrated) in channels.items():
        idx = np.flatnonzero(channel == ch)
        rating[rng.choice(idx, size=unrated, replace=False)] = 99
    base_rate = np.select([room == "superior", room == "suite"], [130.0, 210.0], default=95.0)
    df = pd.DataFrame(
        {
            "booking_channel": channel,
            "room_type": room,
            "nights": rng.integers(1, 11, n),
            "guests": rng.integers(1, 5, n),
            "lead_time_days": rng.gamma(2, 20, n).round().astype(int),
            "nightly_rate_eur": (base_rate * rng.lognormal(0, 0.12, n)).round(2),
            "stay_rating": rating,
        }
    )
    return _shuffled(df, rng)


GENERATORS = {"h5_hotel_stays": h5_hotel_stays}