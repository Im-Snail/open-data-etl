# Open Data ETL Mini-Project: Weather in Portugal

A small ETL workflow in Python (pandas) that collects daily weather data for 5 Portuguese cities and saves a clean CSV for later dashboard use.

## Data source
[Open-Meteo API](https://open-meteo.com/) (no API key needed). Cities: Lisbon, Porto, Faro, Coimbra, Braga. Period: the last 30 days plus today.

## Steps
1. Extract: request daily max/min temperature and precipitation for each city.
2. Transform: rename columns, convert `date` to datetime, drop missing values, compute `temp_avg` and `temp_range`, add `rainy` (precipitation > 1 mm), select columns, sort by city and date.
3. Load: save raw data to `data/raw/weather_raw.csv` (ignored by git) and clean data to `data/processed/output.csv`.

## How to run
```
pip install -r requirements.txt
python -m src.main
```
Then check that `data/processed/output.csv` was created.

## Output
`data/processed/output.csv` has 155 rows (5 cities x 31 days) and the columns: city, date, temp_min, temp_max, temp_avg, temp_range, precip_mm, rainy.

Example rows:

| city | date | temp_min | temp_max | temp_avg | temp_range | precip_mm | rainy |
|---|---|---|---|---|---|---|---|
| Lisbon | 2026-11-11 | 16.1 | 19.4 | 17.8 | 3.3 | 78.2 | True |
| Braga | 2026-11-12 | 14.7 | 16.3 | 15.5 | 1.6 | 61.5 | True |
| Coimbra | 2026-11-21 | 14.4 | 17.2 | 15.8 | 2.8 | 69.1 | True |
