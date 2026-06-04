#  Data Pipeline (ETL)

> A modular, tested **Extract → Transform → Load** pipeline with a built-in data-quality gate that stops bad data before it reaches the warehouse.

<p align="left">
  <img src="https://github.com/Harshalingawale/data-pipeline-etl/actions/workflows/ci.yml/badge.svg" alt="CI" />
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/pandas-Transform-150458?logo=pandas&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLite-Warehouse-003B57?logo=sqlite&logoColor=white" />
  <img src="https://img.shields.io/badge/CI-GitHub%20Actions-2088FF?logo=githubactions&logoColor=white" />
  <img src="https://img.shields.io/badge/tests-pytest-0A9EDC?logo=pytest&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-green" />
</p>

---

## Demo

![ETL pipeline run](assets/demo.gif)

*One command runs the full Extract → Transform → Quality-gate → Load pipeline.*


##  What this demonstrates

Clean data engineering fundamentals: each stage is a small, independently testable module; the orchestrator wires them together with structured logging; and a **quality gate** raises an exception on dirty data so nothing invalid ever lands in the warehouse. The source feed is synthetic (and intentionally dirty — nulls, duplicates, negative quantities) so the cleaning logic has something real to do.

> A verified run cleans ~5,000 raw rows into 4,970 valid orders and builds a 600-row daily-revenue mart by country.

##  Pipeline stages

```
 extract.py        transform.py            quality.py         load.py
┌──────────┐      ┌──────────────┐       ┌────────────┐     ┌──────────────┐
│ raw feed │ ───▶ │ dedupe       │ ────▶ │ assert:    │ ──▶ │ fact_orders  │
│ (dirty)  │      │ drop bad qty │       │ no nulls   │     │ agg_daily_   │
│          │      │ impute price │       │ no dupes   │     │   revenue    │
│          │      │ derive rev   │       │ qty > 0    │     │ (SQLite)     │
└──────────┘      └──────────────┘       └────────────┘     └──────────────┘
                         orchestrated by pipeline/run.py (with logging)
```

| Module | Responsibility |
|---|---|
| `pipeline/extract.py` | Read source (swap in API/DB/S3); generates a dirty synthetic feed for demos |
| `pipeline/transform.py` | Dedupe, drop invalid rows, median-impute prices, derive `revenue`, build daily mart |
| `pipeline/quality.py` | Assertion-based data-quality gate (`DataQualityError` on failure) |
| `pipeline/load.py` | Write tables to SQLite (one-line swap to Postgres) |
| `pipeline/run.py` | Orchestrate the run with structured logging |

##  Quickstart

```bash
git clone https://github.com/harshalingawale/data-pipeline-etl.git
cd data-pipeline-etl
make install
make run        # python -m pipeline.run
```

Output:

```
... | INFO | EXTRACT: reading raw orders  -> 5040 raw rows
... | INFO | TRANSFORM: cleaning + enriching  -> 4970 clean rows
... | INFO | QUALITY: validating  -> all checks passed
... | INFO | LOAD: fact_orders=4970  agg_daily_revenue=600
... | INFO | DONE: {'raw': 5040, 'clean': 4970, 'total_revenue': 1239084.49}
```

Query the warehouse:

```bash
sqlite3 data/warehouse.db "SELECT country, SUM(revenue) FROM agg_daily_revenue GROUP BY country;"
```

##  Tests & CI

```bash
make test
```

The test suite covers cleaning correctness, the aggregate schema, and **both** quality-gate paths (passes on clean data, raises on dirty). CI runs the full pipeline + tests on every push.

##  Productionizing

- **Real sources** — replace `extract()` with your reader (REST, JDBC, S3, Kafka).
- **Real warehouse** — change the SQLite connection in `load.py` to a Postgres/Snowflake URI.
- **Scheduling** — wrap `pipeline.run:run` in an Airflow/Prefect/Dagster task or a cron container.

##  Tech Stack

**Python · pandas · NumPy · SQLite · pytest · GitHub Actions**

##  Roadmap

- [ ] Airflow DAG wrapper
- [ ] Incremental / idempotent loads with watermarks
- [ ] Great Expectations / Pandera schema validation
- [ ] dbt models on top of the warehouse

##  License

MIT © [Harshal Ingawale](https://github.com/harshalingawale)
