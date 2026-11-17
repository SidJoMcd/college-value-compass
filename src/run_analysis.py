
from pathlib import Path

import duckdb

# Locate the project directory.
PROJECT_DIR = Path(__file__).resolve().parents[1]

SQL_FILE = PROJECT_DIR / "sql" / "01_college_value_analysis.sql"

def main():
    # Connect to an in-memory DuckDB database.
    connection = duckdb.connect(database=":memory:")

    # Read the SQL file.
    sql_text = SQL_FILE.read_text()

    # Separate individual SQL queries using semicolons.
    queries = [
        query.strip()
        for query in sql_text.split(";")
        if query.strip()
    ]

    print(f"Found {len(queries)} SQL queries.\n")

    for number, query in enumerate(queries, start=1):
        print("=" * 70)
        print(f"QUERY {number}")
        print("=" * 70)

        result = connection.execute(query).df()

        print(result.to_string(index=False))
        print(f"\nRows returned: {len(result)}\n")

    connection.close()


if __name__ == "__main__":
    main()
