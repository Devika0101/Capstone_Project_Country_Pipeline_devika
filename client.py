
"""Fetch country data from FastAPI, export CSV, and create a scatter plot."""

from pathlib import Path

import pandas as pd
import requests
from visualization import create_scatter_plot


API_URL = "http://127.0.0.1:8000/countries"
OUTPUT_DIR = Path(__file__).resolve().parent


def main():
    # Step 1: Fetch country data from FastAPI.
    try:
        response = requests.get(API_URL, timeout=15)
        response.raise_for_status()

    except requests.RequestException as exc:
        raise SystemExit(
            "Could not reach the API. Start it in another terminal with:\n"
            "python -m uvicorn main:app --reload\n"
            f"Details: {exc}"
        )

    # Step 2: Read the API response.
    data = response.json()

    if not data:
        raise SystemExit(
            "The API returned no countries. "
            "Run python seed_database.py first."
        )

    # Step 3: Convert the response into a DataFrame.
    df = pd.DataFrame(data)

    expected_columns = [
        "country_name",
        "capital",
        "population",
        "area",
    ]

    missing = set(expected_columns) - set(df.columns)

    if missing:
        raise SystemExit(
            f"API response is missing columns: {sorted(missing)}"
        )

    df = df[expected_columns]

    # Step 4: Display the country data.
    print("\nCountry data from the API:\n")
    print(df.to_string(index=False))

    # Step 5: Export the data to a CSV file.
    csv_path = OUTPUT_DIR / "exported_countries.csv"

    df.to_csv(
        csv_path,
        index=False,
        encoding="utf-8",
    )

    print(f"\nCSV saved to: {csv_path}")

    # Step 6: Create the scatter plot using visualization.py.
    chart_path = OUTPUT_DIR / "population_vs_area.png"

    create_scatter_plot(df, chart_path)


if __name__ == "__main__":
    main()
