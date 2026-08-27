import duckdb

from src.sales_queries import (
    top_5_products,
    revenue_by_region,
    best_category_recent_7_days
)


DATABASE_FILE = "data/northstar.duckdb"


def test_sales_table_has_expected_rows():

    con = duckdb.connect(DATABASE_FILE)

    result = con.execute(
        "SELECT COUNT(*) FROM sales"
    ).fetchone()[0]

    assert result == 5084

    con.close()


def test_top_5_products_returns_five_rows():

    con = duckdb.connect(DATABASE_FILE)

    result = top_5_products(con)

    assert len(result) == 5

    con.close()


def test_region_revenue_returns_regions():

    con = duckdb.connect(DATABASE_FILE)

    result = revenue_by_region(con)

    assert len(result) == 5

    assert "region" in result.columns
    assert "total_revenue" in result.columns

    con.close()


def test_recent_category_query_returns_results():

    con = duckdb.connect(DATABASE_FILE)

    result = best_category_recent_7_days(con)

    assert len(result) > 0

    assert "category" in result.columns
    assert "total_revenue" in result.columns

    con.close()
