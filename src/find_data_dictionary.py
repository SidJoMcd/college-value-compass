from pathlib import Path

DATA_DIR = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "raw"
    / "College_Scorecard_Raw_Data_10152026"
)

terms = [
    "EARN_MDN_1YR",
    "EARN_MDN_4YR",
    "NPT4_PUB",
    "C150_4",
    "CIPCODE",
]

for path in DATA_DIR.rglob("*"):
    if not path.is_file():
        continue

    if path.suffix.lower() not in {".yaml", ".yml", ".txt", ".md"}:
        continue

    try:
        content = path.read_text(
            encoding="utf-8", errors="ignore"
        )
    except OSError:
        continue

    found = [term for term in terms if term in content]

    if found:
        print(f"\nFILE: {path.name}")
        print("Matching terms:", ", ".join(found))
