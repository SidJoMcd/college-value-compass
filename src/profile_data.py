from pathlib import Path

import pandas as pd

DATA_DIR = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "raw"
    / "College_Scorecard_Raw_Data_10152026"
)

FILES = [
    "Most-Recent-Cohorts-Institution.csv",
    "Most-Recent-Cohorts-Field-of-Study.csv",
]

MISSING_MARKERS = ["NULL", "PrivacySuppressed", "NA", "PS"]

def inspect_file(filename):
    path = DATA_DIR / filename

    print(f"\n{'=' * 80}")
    print(f"FILE: {filename}")
    print(f"{'=' * 80}")

    # Read a small sample first to inspect column names and example reconds.
    sample = pd.read_csv(
    path,
    nrows=5,
    low_memory=False,
    na_values=MISSING_MARKERS,
    )

    print(f"\nNumber of columns: {len(sample.columns)}")
    print("\nColumn names:")
    print(sample.columns.tolist())

    print("\nSample rows:")
    print(sample.head(3).to_string(index=False))

    # Read the complete file to examine row counts and missing values.
    df = pd.read_csv(
    path,
    low_memory=False,
    na_values=MISSING_MARKERS,
    )

    print(f"\nNumber of rows: {len(df):,}")
    print(f"Number of columns: {len(df.columns):,}")

    print("\nColumns with the most missing values:")
    missing = (
        df.isna()
        .mean()
        .mul(100)
        .sort_values(ascending=False)
        .head(15)
        .round(1)
    )
    print(missing.to_string())


if __name__ == "__main__":
    for filename in FILES:
        inspect_file(filename)
