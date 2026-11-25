from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data" / "raw"
OUT_DIR = ROOT / "data" / "processed"

URL = "https://api.open-meteo.com/v1/forecast"
CITIES = {
    "Lisbon": (38.72, -9.14),
    "Porto": (41.15, -8.61),
    "Faro": (37.02, -7.93),
    "Coimbra": (40.21, -8.43),
    "Braga": (41.55, -8.42),
}


def extract():
    frames = []
    for city, (lat, lon) in CITIES.items():
        params = {
            "latitude": lat,
            "longitude": lon,
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
            "timezone": "Europe/Lisbon",
            "past_days": 30,
            "forecast_days": 1,
        }
        r = requests.get(URL, params=params, timeout=30)
        r.raise_for_status()
        df = pd.DataFrame(r.json()["daily"])
        df["city"] = city
        frames.append(df)
    return pd.concat(frames, ignore_index=True)


def transform(raw):
    df = raw.rename(columns={
        "time": "date",
        "temperature_2m_max": "temp_max",
        "temperature_2m_min": "temp_min",
        "precipitation_sum": "precip_mm",
    })
    df["date"] = pd.to_datetime(df["date"])
    df = df.dropna()
    df["temp_avg"] = ((df["temp_max"] + df["temp_min"]) / 2).round(1)
    df["temp_range"] = (df["temp_max"] - df["temp_min"]).round(1)
    df["rainy"] = df["precip_mm"] > 1
    df = df[["city", "date", "temp_min", "temp_max", "temp_avg", "temp_range", "precip_mm", "rainy"]]
    return df.sort_values(["city", "date"]).reset_index(drop=True)


def load(raw, clean):
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    raw.to_csv(RAW_DIR / "weather_raw.csv", index=False)
    clean.to_csv(OUT_DIR / "output.csv", index=False)


if __name__ == "__main__":
    raw = extract()
    print(raw.shape)
    clean = transform(raw)
    print(clean.shape)
    print(clean.head())
    load(raw, clean)
    print("Saved data/processed/output.csv")
