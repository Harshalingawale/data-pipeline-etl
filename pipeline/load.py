"""Load step: write tables to SQLite (swap the URI for Postgres in prod)."""
from __future__ import annotations
import sqlite3
from pathlib import Path
import pandas as pd

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "warehouse.db"


def load(table: str, df: pd.DataFrame, db_path: Path = DB_PATH) -> int:
    db_path.parent.mkdir(exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        df.to_sql(table, conn, if_exists="replace", index=False)
    return len(df)
