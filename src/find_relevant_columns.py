from pathlib import Path
import pandas as pd

DATA_DIR = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "raw"
    / "College_Scorecard_Raw_Data_10152026"
)

FILES = {
    "INSTITUTION": "Most-Recent-Cohorts-Institution.csv",
    "FIELD_OF_STUDY": "Most-Recent-Cohorts-Field-of-Study.csv",
}

KEYWORDS = [
    "NAME",
    "ID",
    "CIP",
    "MAJOR",
    "PROGRAM",
    "COST",
    "NPT",
    "PRICE",
    "TUITION",
    "GRAD",
    "COMP",
    "COMPLETION",
    "EARN",
    "MDN",
    "MEDIAN",
]

for dataset_name, filename in FILES.items():
    path = DATA_DIR / filename

    # Read only the header; no need to load the entire dataset.
    columns = pd.read_csv(path, nrows=0).columns.tolist()

    print(f"\n{'=' * 70}")
    print(dataset_name)
    print(f"{'=' * 70}")

    for keyword in KEYWORDS:
        matches = [
            column for column in columns
            if keyword in column.upper()
        ]

        if matches:
            print(f"\n{keyword} ({len(matches)} matches):")
            print(", ".join(matches[:40]))

            if len(matches) > 40:
                print(f"... and {len(matches) - 40} more")
