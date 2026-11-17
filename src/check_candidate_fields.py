from pathlib import Path
import pandas as pd

DATA_DIR = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "raw"
    / "College_Scorecard_Raw_Data_10152026"
)

MISSING_MARKERS = ["NULL", "PrivacySuppressed", "NA", "PS"]

CANDIDATES = {
    "Most-Recent-Cohorts-Institution.csv": [
        "UNITID",
        "INSTNM",
        "NPT4_PUB",
        "NPT4_PRIV",
        "TUITIONFEE_IN",
        "TUITIONFEE_OUT",
        "COSTT4_A",
        "COSTT4_P",
        "C150_4",
        "C150_L4",
        "GRADS",
        "CONTROL",
        "ICLEVEL",
        "PREDDEG",
        "RET_FT4",
    ],
    "Most-Recent-Cohorts-Field-of-Study.csv": [
        "UNITID",
        "CIPCODE",
        "CIPDESC",
        "EARN_MDN_1YR",
        "EARN_MDN_4YR",
        "EARN_COUNT_WNE_1YR",
        "EARN_COUNT_WNE_4YR",
        "CREDLEV",
        "CREDDESC",
        "EARN_MDN_4YR",
        "IPEDSCOUNT2",
        "DEBT_ALL_STGP_ANY_MDN",
    ],
}

for filename, candidates in CANDIDATES.items():
    path = DATA_DIR / filename

    # Read the header first so we skip fields that don't exist.
    available_columns = pd.read_csv(path, nrows=0).columns
    selected = [col for col in candidates if col in available_columns]
    missing_columns = [col for col in candidates if col not in available_columns]

    df = pd.read_csv(
        path,
        usecols=selected,
        low_memory=False,
        na_values=MISSING_MARKERS,
    )

    print(f"\n{'=' * 70}")
    print(filename)
    print(f"{'=' * 70}")
    print(f"Rows: {len(df):,}")

    if missing_columns:
        print("Candidate columns not found:", ", ".join(missing_columns))

    print("\nMissing values by column:")
    print((df.isna().mean() * 100).round(1).to_string())

    print("\nSample values:")
    print(df.head(3).to_string(index=False))
