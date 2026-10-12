"""SQLite database manager with CRUD operations."""
import sqlite3
from pathlib import Path
from typing import Any

DB_PATH = Path(__file__).resolve().parent / "countries.db"


class CountryDatabaseManager:
    def __init__(self, db_path: str | Path = DB_PATH):
        self.db_path = str(db_path)
        self.create_table()

    def _connect(self):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def create_table(self) -> None:
        with self._connect() as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS countries (
                    country_name TEXT PRIMARY KEY,
                    capital TEXT NOT NULL,
                    population INTEGER NOT NULL CHECK(population >= 0),
                    area REAL NOT NULL CHECK(area >= 0)
                )
            """)

    @staticmethod
    def _row_to_dict(row) -> dict[str, Any] | None:
        return dict(row) if row is not None else None

    def create_country(self, country: dict) -> dict:
        """Insert a country. Raises ValueError if the name already exists."""
        try:
            with self._connect() as connection:
                connection.execute(
                    "INSERT INTO countries (country_name, capital, population, area) VALUES (?, ?, ?, ?)",
                    (country["country_name"], country["capital"], int(country["population"]), float(country["area"])),
                )
        except sqlite3.IntegrityError as exc:
            raise ValueError(f"Country {country['country_name']!r} already exists or has invalid data.") from exc
        return self.get_country(country["country_name"])

    def upsert_country(self, country: dict) -> None:
        """Insert a scraped record or refresh it if the country already exists."""
        with self._connect() as connection:
            connection.execute("""
                INSERT INTO countries (country_name, capital, population, area)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(country_name) DO UPDATE SET
                    capital = excluded.capital,
                    population = excluded.population,
                    area = excluded.area
            """, (country["country_name"], country["capital"], int(country["population"]), float(country["area"])))

    def get_all_countries(self) -> list[dict]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT country_name, capital, population, area FROM countries ORDER BY country_name"
            ).fetchall()
        return [dict(row) for row in rows]

    def get_country(self, country_name: str) -> dict | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT country_name, capital, population, area FROM countries WHERE country_name = ?",
                (country_name,),
            ).fetchone()
        return self._row_to_dict(row)

    def update_country(self, country_name: str, updates: dict) -> dict | None:
        existing = self.get_country(country_name)
        if existing is None:
            return None
        merged = {**existing, **updates}
        with self._connect() as connection:
            connection.execute("""
                UPDATE countries
                SET capital = ?, population = ?, area = ?
                WHERE country_name = ?
            """, (merged["capital"], int(merged["population"]), float(merged["area"]), country_name))
        return self.get_country(country_name)

    def delete_country(self, country_name: str) -> bool:
        with self._connect() as connection:
            cursor = connection.execute(
                "DELETE FROM countries WHERE country_name = ?", (country_name,)
            )
            return cursor.rowcount > 0

    def save_scraped_countries(self, countries: list[dict]) -> int:
        for country in countries:
            self.upsert_country(country)
        return len(countries)
