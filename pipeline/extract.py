"""Extract step. Generates a synthetic raw orders feed (or reads a CSV).

In production, replace `generate_raw_orders` with an API/DB/S3 reader — the
rest of the pipeline is source-agnostic.
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd

RAW_PATH = Path(__file__).resolve().parent.parent / "data" / "raw_orders.csv"


def generate_raw_orders(n: int = 5000, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    products = ["Sensor-A", "Sensor-B", "Controller", "Cable", "Gateway"]
    countries = ["DE", "IN", "US", "FR", "JP"]
    dates = pd.to_datetime("2025-01-01") + pd.to_timedelta(rng.integers(0, 120, n), unit="D")
    df = pd.DataFrame({
        "order_id": np.arange(1, n + 1),
        "order_date": dates,
        "product": rng.choice(products, n),
        "country": rng.choice(countries, n),
        "quantity": rng.integers(1, 10, n),
        "unit_price": rng.normal(50, 15, n).round(2),
    })
    # Inject realistic dirt: nulls, dupes, negatives
    df.loc[rng.choice(n, 60, replace=False), "unit_price"] = np.nan
    df.loc[rng.choice(n, 30, replace=False), "quantity"] = -1
    df = pd.concat([df, df.sample(40, random_state=seed)], ignore_index=True)
    return df


def extract() -> pd.DataFrame:
    if RAW_PATH.exists():
        return pd.read_csv(RAW_PATH, parse_dates=["order_date"])
    df = generate_raw_orders()
    RAW_PATH.parent.mkdir(exist_ok=True)
    df.to_csv(RAW_PATH, index=False)
    return df
