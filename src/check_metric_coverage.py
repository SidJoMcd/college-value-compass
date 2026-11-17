
from pathlib import Path

import pandas as pd

DATA_DIR = Path("data/raw/College_Scorecard_Raw_Data_10152026")

FILE = DATA_DIR / "Most-Recent-Cohorts-Institution.csv"

COLUMNS = [
    "UNITID",
    "INSTNM",
    "CONTROL",
    "ICLEVEL",
    "PREDDEG",
    "NPT4_PUB",
    "NPT4_PRIV",
    "C150_4",
]

df = pd.read_csv(
    FILE,
    usecols=COLUMNS,
    na_values=["NULL", "PrivacySuppressed", "NA", "PS"],
)

# Keep institutions classified as four-year.
four_year = df[df["ICLEVEL"] == 1].copy()

# Select the applicable net-price field based on ownership:
# CONTROL = 1: public
# CONTROL = 2: private nonprofit
# CONTROL = 3: private for-profit
four_year["NET_PRICE"] = pd.NA

public = four_year["CONTROL"] == 1
private_nonprofit = four_year["CONTROL"] == 2

four_year.loc[public, "NET_PRICE"] = four_year.loc[public, "NPT4_PUB"]
four_year.loc[private_nonprofit, "NET_PRICE"] = (
    four_year.loc[private_nonprofit, "NPT4_PRIV"]
)

# Convert the selected price field to a numeric column.
four_year["NET_PRICE"] = pd.to_numeric(
    four_year["NET_PRICE"], errors="coerce"
)

print(f"Total institutions: {len(df):,}")
print(f"Four-year institutions: {len(four_year):,}")

print("\nFour-year institutions by ownership:")
print(four_year["CONTROL"].value_counts(dropna=False).sort_index())

print("\nMetric coverage among four-year institutions:")
print(f"Net price available: {four_year['NET_PRICE'].notna().sum():,}")
print(f"Completion rate available: {four_year['C150_4'].notna().sum():,}")

both_available = (
    four_year["NET_PRICE"].notna()
    & four_year["C150_4"].notna()
)


print("\nCoverage by ownership:")
for control, label in [
    (1, "Public"),
    (2, "Private nonprofit"),
    (3, "Private for-profit"),
]:
    group = four_year[four_year["CONTROL"] == control]
    both = group["NET_PRICE"].notna() & group["C150_4"].notna()

    print(f"\n{label}: {len(group):,} institutions")
    print(f"  Net price available: {group['NET_PRICE'].notna().sum():,}")
    print(f"  Completion rate available: {group['C150_4'].notna().sum():,}")
    print(f"  Both available: {both.sum():,}")

print(f"Both metrics available: {both_available.sum():,}")

print("\nSample institutions with both metrics:")
print(
    four_year.loc[
        both_available,
        ["INSTNM", "CONTROL", "NET_PRICE", "C150_4"],
    ]
    .head(10)
    .to_string(index=False)
)
