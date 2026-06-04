"""Orchestrate the ETL run with structured logging.

    python -m pipeline.run
"""
from __future__ import annotations
import logging
from .extract import extract
from .transform import clean, daily_revenue
from .quality import validate_clean_orders
from .load import load

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
log = logging.getLogger("etl")


def run() -> dict:
    log.info("EXTRACT: reading raw orders")
    raw = extract()
    log.info("  -> %d raw rows", len(raw))

    log.info("TRANSFORM: cleaning + enriching")
    orders = clean(raw)
    log.info("  -> %d clean rows", len(orders))

    log.info("QUALITY: validating")
    validate_clean_orders(orders)
    log.info("  -> all checks passed")

    log.info("AGGREGATE: daily revenue by country")
    agg = daily_revenue(orders)

    log.info("LOAD: writing to warehouse")
    n1 = load("fact_orders", orders)
    n2 = load("agg_daily_revenue", agg)
    log.info("  -> fact_orders=%d  agg_daily_revenue=%d", n1, n2)

    summary = {"raw": len(raw), "clean": len(orders), "agg_rows": len(agg),
               "total_revenue": float(orders["revenue"].sum().round(2))}
    log.info("DONE: %s", summary)
    return summary


if __name__ == "__main__":
    run()
