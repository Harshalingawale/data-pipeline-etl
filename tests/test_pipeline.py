import pandas as pd
from pipeline.extract import generate_raw_orders
from pipeline.transform import clean, daily_revenue
from pipeline.quality import validate_clean_orders, DataQualityError


def test_clean_removes_dupes_and_bad_rows():
    raw = generate_raw_orders(n=1000)
    out = clean(raw)
    assert out["order_id"].duplicated().sum() == 0
    assert (out["quantity"] > 0).all()
    assert out["revenue"].isna().sum() == 0


def test_quality_gate_passes_on_clean():
    out = clean(generate_raw_orders(n=500))
    assert validate_clean_orders(out)["non_empty"]


def test_quality_gate_raises_on_dirty():
    bad = pd.DataFrame({"order_id": [1, 1], "quantity": [1, 1], "revenue": [10.0, None]})
    try:
        validate_clean_orders(bad)
        assert False, "should have raised"
    except DataQualityError:
        assert True


def test_aggregate_shape():
    agg = daily_revenue(clean(generate_raw_orders(n=800)))
    assert {"day", "country", "orders", "revenue"}.issubset(agg.columns)
