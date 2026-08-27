import pandas as pd


INPUT_FILE = "data/sales.csv"
OUTPUT_FILE = "data/clean_sales.csv"


def clean_sales(input_file, output_file):

    # 1. Load raw data
    df = pd.read_csv(input_file)

    print("Original rows:", len(df))

    # 2. Remove exact duplicate rows
    df = df.drop_duplicates()

    print("After removing exact duplicates:", len(df))

    # 3. Normalize order dates
    df["order_date"] = pd.to_datetime(
        df["order_date"],
        format="mixed"
    )

    # 4. Build product_id -> product_name mapping
    product_name_map = (
        df.dropna(subset=["product_name"])
        .groupby("product_id")["product_name"]
        .first()
    )

    # 5. Build product_id -> unit_price mapping
    price_map = (
        df.dropna(subset=["unit_price"])
        .groupby("product_id")["unit_price"]
        .first()
    )

    # 6. Fill missing product names
    df["product_name"] = (
        df["product_name"]
        .fillna(df["product_id"].map(product_name_map))
    )

    # 7. Fill missing unit prices
    df["unit_price"] = (
        df["unit_price"]
        .fillna(df["product_id"].map(price_map))
    )

    # 8. Remove rows where quantity is missing
    df = df.dropna(subset=["quantity"])

    # 9. Calculate revenue
    df["revenue"] = df["quantity"] * df["unit_price"]

    # 10. Save cleaned data
    df.to_csv(output_file, index=False)

    print("Final rows:", len(df))
    print("Saved to:", output_file)


if __name__ == "__main__":
    clean_sales(INPUT_FILE, OUTPUT_FILE)
