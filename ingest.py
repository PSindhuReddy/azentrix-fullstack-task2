# ingest.py
# This file downloads raw data from 2 sources and saves them to landing_zone folder

import requests
import pandas as pd
import logging
import os
from datetime import datetime

# ── LOGGING SETUP ──────────────────────────────
logging.basicConfig(
    filename="logs/ingest.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ── SOURCE 1: WORLD BANK API (GDP Data) ────────
def ingest_gdp_api():
    logging.info("Ingesting GDP data from World Bank API...")

    url = "https://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.CD?format=json&per_page=300&mrv=1"
    response = requests.get(url, timeout=30)

    if response.status_code != 200:
        raise Exception(f"API call failed: {response.status_code}")

    raw = response.json()
    records = raw[1]

    df = pd.DataFrame([{
        "country_name": r["country"]["value"],
        "country_code": r["countryiso3code"],
        "year":         r["date"],
        "gdp_usd":      r["value"]
    } for r in records if r["value"] is not None])

    # Save raw data to landing zone
    path = "landing_zone/gdp_raw.csv"
    df.to_csv(path, index=False)
    logging.info(f"GDP data saved to {path} — {len(df)} rows")
    print(f"✅ GDP data ingested — {len(df)} rows")

# ── SOURCE 2: POPULATION CSV (Our World in Data) ──
def ingest_population_csv():
    logging.info("Ingesting Population data from CSV...")

    url = "https://raw.githubusercontent.com/datasets/population/master/data/population.csv"
    response = requests.get(url, timeout=30)

    if response.status_code != 200:
        raise Exception(f"CSV download failed: {response.status_code}")

    # Save raw CSV to landing zone
    path = "landing_zone/population_raw.csv"
    with open(path, "wb") as f:
        f.write(response.content)

    df = pd.read_csv(path)
    logging.info(f"Population data saved to {path} — {len(df)} rows")
    print(f"✅ Population data ingested — {len(df)} rows")

# ── RUN BOTH ───────────────────────────────────
if __name__ == "__main__":
    print("Starting data ingestion...")
    ingest_gdp_api()
    ingest_population_csv()
    print("✅ All data saved to landing_zone folder!")