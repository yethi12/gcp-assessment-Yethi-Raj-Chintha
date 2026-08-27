import pandas as pd

df = pd.read_csv("data/sales.csv")

print(df.shape)
print(df.info())
print(df.head())
print(df.isna().sum())
print(df.describe(include="all"))