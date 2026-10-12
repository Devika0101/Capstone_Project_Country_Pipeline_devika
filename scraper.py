"""Scrape the first 20 countries from Scrape This Site."""
import requests
from bs4 import BeautifulSoup

URL = "https://www.scrapethissite.com/pages/simple/"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; CountryDataCapstone/1.0)"}


def scrape_countries(limit: int = 20) -> list[dict]:
    """Return up to `limit` country records from the target website."""
    response = requests.get(URL, headers=HEADERS, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    countries = []
    for item in soup.select(".country"):
        name_el = item.select_one(".country-name")
        capital_el = item.select_one(".country-capital")
        population_el = item.select_one(".country-population")
        area_el = item.select_one(".country-area")

        if not all([name_el, capital_el, population_el, area_el]):
            continue

        name = name_el.get_text(" ", strip=True)
        capital = capital_el.get_text(" ", strip=True)
        population_text = population_el.get_text(" ", strip=True).replace(",", "")
        area_text = area_el.get_text(" ", strip=True).replace(",", "")

        try:
            population = int(float(population_text))
            area = float(area_text)
        except ValueError:
            print(f"Skipping invalid numeric values for {name!r}")
            continue

        countries.append({
            "country_name": name,
            "capital": capital,
            "population": population,
            "area": area,
        })
        if len(countries) >= limit:
            break

    if not countries:
        raise RuntimeError("No country records were scraped. Check the website or its HTML structure.")
    return countries


if __name__ == "__main__":
    records = scrape_countries(20)
    print(f"Scraped {len(records)} countries:")
    for record in records:
        print(record)
