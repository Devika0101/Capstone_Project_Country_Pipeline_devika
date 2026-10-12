# End-to-End Country Data Pipeline & Analytics System

A Python capstone project that scrapes the first 20 country records from [Scrape This Site](https://www.scrapethissite.com/pages/simple/), stores them in SQLite, exposes CRUD operations through FastAPI, and exports data to CSV with a population-versus-area scatter plot.

## Features

- Web scraping with `requests` and `BeautifulSoup`
- SQLite database with country name as the natural primary key
- Object-oriented database manager with Create, Read, Update, and Delete methods
- FastAPI REST API with five required endpoints
- Pandas DataFrame and CSV export
- Matplotlib scatter plot saved as PNG

## Requirements

- Python 3.10 or newer
- VS Code (recommended)

## Setup on Windows (PowerShell)

Open this folder in VS Code and open **Terminal → New Terminal**.

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, run this in the same terminal and activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

If the `python` command is not recognized, resolve the Python installation/PATH issue before continuing.

## Run the project

### 1. Scrape and populate the database

```powershell
python scraper.py
python seed_database.py
```

`countries.db` is created automatically. Running the seeding script again refreshes matching records rather than creating duplicates.

### 2. Start the API

In terminal 1 (with `.venv` activated):

```powershell
python -m uvicorn main:app --reload
```

Keep this terminal running. The API base address is `http://127.0.0.1:8000`.

### 3. Test the API

Open `http://127.0.0.1:8000/docs` in a browser. Expand each endpoint and select **Try it out**. The interactive docs can test GET, POST, PUT, and DELETE requests.

Endpoints:
- `GET /countries`
- `GET /countries/{country_name}`
- `POST /countries`
- `PUT /countries/{country_name}`
- `DELETE /countries/{country_name}`

Example POST body:

```json
{
  "country_name": "Exampleland",
  "capital": "Example City",
  "population": 123456,
  "area": 1234.5
}
```

Use a unique country name for POST because country name is the primary key. This is only a test record; delete it afterward if you add it.

### 4. Run the client, CSV export, and chart

Keep the API running. Open terminal 2 in VS Code, activate `.venv` there too, then run:

```powershell
.\.venv\Scripts\Activate.ps1
python client.py
```

The client creates:
- `exported_countries.csv`
- `population_vs_area.png`

## Project structure

```text
country-data-pipeline/
├── .gitignore
├── README.md
├── requirements.txt
├── scraper.py
├── database.py
├── seed_database.py
├── main.py
└── client.py
```

Generated files (`countries.db`, CSV, PNG) are created when you run the project. They are ignored by Git by default; remove their entries from `.gitignore` if your evaluator explicitly requires these generated outputs to be committed.

## Troubleshooting

- **API connection refused:** Start the API with `python -m uvicorn main:app --reload` and leave it running.
- **No countries returned:** Run `python seed_database.py` before starting the client.
- **Module not found:** Activate `.venv` and run `pip install -r requirements.txt`.
- **Website/network error:** Check your internet connection and try again later. The scraper intentionally fails clearly instead of silently using made-up data.

## GitHub submission

1. Create a new public GitHub repository named `country-data-pipeline` (unless your instructor specifies another visibility).
2. Upload the project source files and README. Do not upload `.venv/` or secrets.
3. Copy the repository URL and submit it.
4. Before submitting, verify that the README setup and run instructions work from a fresh terminal.
