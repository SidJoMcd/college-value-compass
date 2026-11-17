
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
    "TUITIONFEE_IN",
    "TUITIONFEE_OUT",
    "NPT4_PUB",
    "NPT4_PRIV",
    "COSTT4_A",
    "COSTT4_P",
    "C150_4",
]

df = pd.read_csv(
    FILE,
    usecols=COLUMNS,
    na_values=["NULL", "PrivacySuppressed", "NA", "PS"],
)

names = [
    "Career Networks Institute",
    "United States Air Force Academy",
    "United States Coast Guard Academy",
    "United States Naval Academy",
    "United States Military Academy",
    "Curtis Institute of Music",
    "Ricketts Great Books College",
    "Calvin University - Handlon Campus",
]

matches = df[df["INSTNM"].isin(names)]

print(matches.to_string(index=False))
