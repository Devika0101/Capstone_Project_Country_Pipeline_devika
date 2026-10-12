
"""Scrape and store the first 20 countries in SQLite."""

from database import CountryDatabaseManager
from scraper import scrape_countries


def main():
    countries = scrape_countries(limit=20)

    db = CountryDatabaseManager()
    count = db.save_scraped_countries(countries)

    print(f"Saved/refreshed {count} country records in countries.db.")
    print(
        f"Total records currently in database: "
        f"{len(db.get_all_countries())}"
    )


if __name__ == "__main__":
    main()
