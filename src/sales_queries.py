import duckdb


DATABASE_FILE = "data/northstar.duckdb"


def top_5_products(con):
    query = """
        SELECT
            product_id,
            product_name,
            SUM(revenue) AS total_revenue
        FROM sales
        GROUP BY product_id, product_name
        ORDER BY total_revenue DESC
        LIMIT 5
    """

    return con.execute(query).fetchdf()


def revenue_by_region(con):
    query = """
        SELECT
            region,
            SUM(revenue) AS total_revenue
        FROM sales
        GROUP BY region
        ORDER BY total_revenue DESC
    """

    return con.execute(query).fetchdf()


def best_category_recent_7_days(con):
    query = """
        WITH latest AS (
            SELECT MAX(order_date) AS latest_order_date
            FROM sales
        )

        SELECT
            category,
            SUM(revenue) AS total_revenue
        FROM sales, latest
        WHERE order_date >= latest_order_date - INTERVAL '7 days'
          AND order_date < latest_order_date
        GROUP BY category
        ORDER BY total_revenue DESC
    """

    return con.execute(query).fetchdf()


def get_sales_answer(question):

    con = duckdb.connect(DATABASE_FILE)

    question_lower = question.lower()

    if "region" in question_lower:
        result = revenue_by_region(con)

        answer = "Total revenue by region:\n\n"

        for _, row in result.iterrows():
            answer += (
                f"- {row['region']}: "
                f"{row['total_revenue']:.2f}\n"
            )

    elif (
        "category" in question_lower
        and (
            "7 day" in question_lower
            or "7 days" in question_lower
            or "recent" in question_lower
        )
    ):
        result = best_category_recent_7_days(con)

        if len(result) > 0:
            top = result.iloc[0]

            answer = (
                f"The highest-revenue category in the "
                f"7-day period before the latest order date "
                f"is {top['category']} with revenue of "
                f"{top['total_revenue']:.2f}."
            )
        else:
            answer = "No sales were found for the requested period."

    else:
        result = top_5_products(con)

        answer = "Top 5 products by total revenue:\n\n"

        for _, row in result.iterrows():
            answer += (
                f"- {row['product_name']} "
                f"({row['product_id']}): "
                f"{row['total_revenue']:.2f}\n"
            )

    con.close()

    return answer


if __name__ == "__main__":

    question = input("Enter a sales question: ")

    print("\n=== ANSWER ===")
    print(get_sales_answer(question))
