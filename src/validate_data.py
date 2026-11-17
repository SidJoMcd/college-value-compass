
from pathlib import Path

import pandas as pd

FILE = Path("data/processed/college_metrics.csv")

df = pd.read_csv(FILE)

print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")
print(f"Duplicate UNITID values: {df['UNITID'].duplicated().sum():,}")

print("\nMissing values:")
print(df.isna().sum().to_string())

print("\nNumeric metric ranges:")
for column in ["NET_PRICE", "TUITIONFEE_IN", "TUITIONFEE_OUT", "C150_4", "RET_FT4"]:
    print(f"\n{column}")
    print(df[column].describe().to_string())

print("\nCompletion rates outside 0–1:")
invalid_completion = df["C150_4"].notna() & ~df["C150_4"].between(0, 1)
print(invalid_completion.sum())

print("\nRetention values outside 0–1:")
invalid_retention = df["RET_FT4"].notna() & ~df["RET_FT4"].between(0, 1)
print(invalid_retention.sum())

print("\nNegative net prices:")
print((df["NET_PRICE"].dropna() < 0).sum())
