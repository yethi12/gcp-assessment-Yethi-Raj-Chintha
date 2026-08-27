import pandas as pd

df = pd.read_csv("data/sales.csv")

print("\n=== EXACT DUPLICATE ROWS ===")
duplicates = df[df.duplicated(keep=False)]
print("Number of duplicate rows:", len(duplicates))
print(duplicates.sort_values(list(df.columns)).to_string(index=False))

print("\n=== NEGATIVE QUANTITIES ===")
negative_qty = df[df["quantity"] < 0]
print("Number of negative quantity rows:", len(negative_qty))
print(negative_qty.to_string(index=False))

print("\n=== MISSING PRODUCT NAMES ===")
missing_product = df[df["product_name"].isna()]
print("Number:", len(missing_product))
print(missing_product.to_string(index=False))

print("\n=== MISSING UNIT PRICES ===")
missing_price = df[df["unit_price"].isna()]
print("Number:", len(missing_price))
print(missing_price.to_string(index=False))

print("\n=== MISSING QUANTITIES ===")
missing_qty = df[df["quantity"].isna()]
print("Number:", len(missing_qty))
print(missing_qty.to_string(index=False))

print("\n=== ORDER ID DUPLICATES ===")
order_counts = df["order_id"].value_counts()
duplicate_orders = order_counts[order_counts > 1]
print("Number of order IDs appearing more than once:", len(duplicate_orders))
print(duplicate_orders.to_string())

print("\n=== PRODUCT ID CONSISTENCY ===")

product_check = df.groupby("product_id").agg(
    product_names=("product_name", lambda x: x.dropna().unique().tolist()),
    prices=("unit_price", lambda x: x.dropna().unique().tolist()),
    categories=("category", lambda x: x.dropna().unique().tolist())
)

print(product_check.to_string())

print("\n=== DATE VALUES ===")
print("Unique date values:", df["order_date"].nunique())
print("First 20 dates:")
print(df["order_date"].head(20).to_string(index=False))

print("\n=== LATEST DATE AS TEXT ===")
print(df["order_date"].max())
