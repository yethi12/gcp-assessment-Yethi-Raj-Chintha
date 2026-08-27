import duckdb


DATABASE_FILE = "data/northstar.duckdb"


con = duckdb.connect(DATABASE_FILE)

print("\n=== TABLES ===")
print(con.execute("SHOW TABLES").fetchall())

print("\n=== ROW COUNT ===")
print(
    con.execute("SELECT COUNT(*) FROM sales").fetchone()[0]
)

print("\n=== SAMPLE DATA ===")
print(
    con.execute("""
        SELECT
            order_id,
            order_date,
            product_id,
            product_name,
            quantity,
            unit_price,
            revenue
        FROM sales
        LIMIT 5
    """).fetchdf())

print("\n=== DATE RANGE ===")
print(
    con.execute("""
        SELECT
            MIN(order_date),
            MAX(order_date)
        FROM sales
    """).fetchone()
)

con.close()
