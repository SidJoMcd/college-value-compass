
from pathlib import Path

import pandas as pd

FILE = Path("data/processed/college_metrics.csv")
df = pd.read_csv(FILE)

tuition_columns = ["TUITIONFEE_IN", "TUITIONFEE_OUT"]

for column in tuition_columns:
    print(f"\n{'=' * 65}")
    print(f"{column}")
    print("=" * 65)

    values = df[column].dropna()

    print(f"Reported values: {len(values):,}")
    print(f"Zero values: {(values == 0).sum():,}")
    print(f"Above $100,000: {(values > 100_000).sum():,}")

    print("\nLowest nonzero values:")
    print(
        df.loc[df[column].notna() & (df[column] > 0),
               ["INSTNM", "CONTROL", column]]
        .sort_values(column)
        .head(10)
        .to_string(index=False)
    )

    print("\nHighest values:")
    print(
        df.loc[df[column].notna(),
               ["INSTNM", "CONTROL", column]]
        .sort_values(column, ascending=False)
        .head(10)
        .to_string(index=False)
    )

    print("\nInstitutions reporting zero:")
    print(
        df.loc[df[column] == 0,
               ["INSTNM", "CONTROL", column]]
        .head(15)
        .to_string(index=False)
    )
