"""Lightweight data-quality gate. Raises on failure so bad data never lands."""
from __future__ import annotations
import pandas as pd


class DataQualityError(Exception):
    pass


def validate_clean_orders(df: pd.DataFrame) -> dict:
    checks = {
        "no_null_revenue": int(df["revenue"].isna().sum()) == 0,
        "positive_quantity": bool((df["quantity"] > 0).all()),
        "no_duplicate_ids": int(df["order_id"].duplicated().sum()) == 0,
        "non_empty": len(df) > 0,
    }
    failed = [k for k, ok in checks.items() if not ok]
    if failed:
        raise DataQualityError(f"Data quality checks failed: {failed}")
    return checks
