import duckdb


DATABASE_FILE = "data/northstar.duckdb"
CLEAN_SALES_FILE = "data/clean_sales.csv"


def create_sales_table():
    con = duckdb.connect(DATABASE_FILE)

    con.execute("DROP TABLE IF EXISTS sales")

    con.execute("""
        CREATE TABLE sales AS
        SELECT *
        FROM read_csv_auto(?)
    """, [CLEAN_SALES_FILE])

    row_count = con.execute(
        "SELECT COUNT(*) FROM sales"
    ).fetchone()[0]

    print("Sales table created successfully.")
    print("Rows in sales table:", row_count)

    con.close()


if __name__ == "__main__":
    create_sales_table()
