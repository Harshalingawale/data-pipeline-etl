"""Transform step: clean, validate, enrich, aggregate."""
from __future__ import annotations
import pandas as pd


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop_duplicates(subset="order_id").copy()
    df = df[df["quantity"] > 0]                      # drop invalid quantities
    df["unit_price"] = df["unit_price"].fillna(df.groupby("product")["unit_price"].transform("median"))
    df["revenue"] = (df["quantity"] * df["unit_price"]).round(2)
    df["order_date"] = pd.to_datetime(df["order_date"])
    return df


def daily_revenue(df: pd.DataFrame) -> pd.DataFrame:
    out = (df.groupby([df["order_date"].dt.date, "country"])
             .agg(orders=("order_id", "count"), revenue=("revenue", "sum"))
             .reset_index()
             .rename(columns={"order_date": "day"}))
    out["revenue"] = out["revenue"].round(2)
    return out
