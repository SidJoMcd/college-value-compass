
from pathlib import Path

import pandas as pd

DATA_DIR = Path("data/raw/College_Scorecard_Raw_Data_10152026")
INPUT_FILE = DATA_DIR / "Most-Recent-Cohorts-Institution.csv"
OUTPUT_DIR = Path("data/processed")
OUTPUT_FILE = OUTPUT_DIR / "college_metrics.csv"

COLUMNS = [
    "UNITID",
    "INSTNM",
    "CONTROL",
    "ICLEVEL",
    "PREDDEG",
    "NPT4_PUB",
    "NPT4_PRIV",
    "TUITIONFEE_IN",
    "TUITIONFEE_OUT",
    "C150_4",
    "RET_FT4",
]

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(
        INPUT_FILE,
        usecols=COLUMNS,
        na_values=["NULL", "PrivacySuppressed", "NA", "PS"],
    )

    # Filter for four-year, predominantly bachelor's-degree institutions
    df = df.loc[
        (df["ICLEVEL"] == 1) &
        (df["PREDDEG"] == 3)
    ].copy()

    # Select net price for public and private nonprofit institutions.
    df["NET_PRICE"] = pd.NA

    public = df["CONTROL"] == 1
    private_nonprofit = df["CONTROL"] == 2

    df.loc[public, "NET_PRICE"] = df.loc[public, "NPT4_PUB"]
    df.loc[private_nonprofit, "NET_PRICE"] = df.loc[
        private_nonprofit, "NPT4_PRIV"
    ]

    df["NET_PRICE"] = pd.to_numeric(df["NET_PRICE"], errors="coerce")

    # Keep the cleaned analytical fields.
    output_columns = [
        "UNITID",
        "INSTNM",
        "CONTROL",
        "ICLEVEL",
        "PREDDEG",
        "NET_PRICE",
        "TUITIONFEE_IN",
        "TUITIONFEE_OUT",
        "C150_4",
        "RET_FT4",
    ]

    cleaned = df[output_columns].copy()

    cleaned.to_csv(OUTPUT_FILE, index=False)

    both_available = (
        cleaned["NET_PRICE"].notna()
        & cleaned["C150_4"].notna()
    )

    print(f"Input institutions: {len(pd.read_csv(INPUT_FILE, usecols=['UNITID'])):,}")
    print("Four-year, predominantly bachelor's-degree institutions:", len(df))
    print(f"Net price available: {cleaned['NET_PRICE'].notna().sum():,}")
    print(f"Completion rate available: {cleaned['C150_4'].notna().sum():,}")
    print(f"Both metrics available: {both_available.sum():,}")
    print(f"Saved cleaned data to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
