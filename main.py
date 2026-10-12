"""FastAPI service for country records."""
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from database import CountryDatabaseManager

app = FastAPI(
    title="Country Data Pipeline API",
    description="CRUD API for the first 20 scraped country records.",
    version="1.0.0",
)
db = CountryDatabaseManager()


class CountryCreate(BaseModel):
    country_name: str = Field(min_length=1, max_length=100)
    capital: str = Field(min_length=1, max_length=100)
    population: int = Field(ge=0)
    area: float = Field(ge=0)


class CountryUpdate(BaseModel):
    capital: str | None = Field(default=None, min_length=1, max_length=100)
    population: int | None = Field(default=None, ge=0)
    area: float | None = Field(default=None, ge=0)


@app.get("/")
def home():
    return {"message": "Country Data Pipeline API is running", "docs": "/docs"}


@app.get("/countries")
def get_countries():
    return db.get_all_countries()


@app.get("/countries/{country_name}")
def get_country(country_name: str):
    country = db.get_country(country_name)
    if country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return country


@app.post("/countries", status_code=status.HTTP_201_CREATED)
def create_country(country: CountryCreate):
    try:
        return db.create_country(country.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@app.put("/countries/{country_name}")
def update_country(country_name: str, updates: CountryUpdate):
    update_data = updates.model_dump(exclude_unset=True, exclude_none=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="Provide at least one field to update")
    country = db.update_country(country_name, update_data)
    if country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return country


@app.delete("/countries/{country_name}")
def delete_country(country_name: str):
    deleted = db.delete_country(country_name)
    if not deleted:
        raise HTTPException(status_code=404, detail="Country not found")
    return {"message": f"{country_name} deleted successfully"}
