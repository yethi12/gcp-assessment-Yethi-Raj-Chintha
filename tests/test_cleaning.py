import pandas as pd


def test_cleaned_sales_file_exists():

    df = pd.read_csv(
        "data/clean_sales.csv"
    )

    assert len(df) == 5084


def test_quantity_has_no_missing_values():

    df = pd.read_csv(
        "data/clean_sales.csv"
    )

    assert df["quantity"].isna().sum() == 0


def test_revenue_column_exists():

    df = pd.read_csv(
        "data/clean_sales.csv"
    )

    assert "revenue" in df.columns


def test_revenue_is_calculated():

    df = pd.read_csv(
        "data/clean_sales.csv"
    )

    sample = df.iloc[0]

    expected = sample["quantity"] * sample["unit_price"]

    assert abs(sample["revenue"] - expected) < 0.0001
