# transform.py
# This file reads raw data from landing_zone, cleans it, 
# and saves it as Parquet files in the transformed folder

import pandas as pd
import logging
from datetime import datetime

# ── LOGGING SETUP ──────────────────────────────
logging.basicConfig(
    filename="logs/transform.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ── TRANSFORM GDP DATA ─────────────────────────
def transform_gdp():
    logging.info("Transforming GDP data...")

    # Read raw file from landing zone
    df = pd.read_csv("landing_zone/gdp_raw.csv")

    # Clean nulls
    df = df.dropna(subset=["gdp_usd"])

    # Fix data types
    df["year"]    = df["year"].astype(int)
    df["gdp_usd"] = pd.to_numeric(df["gdp_usd"], errors="coerce")

    # New Column 1: GDP in Trillions
    df["gdp_trillion"] = (df["gdp_usd"] / 1_000_000_000_000).round(4)

    # New Column 2: Economy Size
    def categorize(gdp):
        if gdp >= 1_000_000_000_000:
            return "Large Economy"
        elif gdp >= 100_000_000_000:
            return "Medium Economy"
        else:
            return "Small Economy"

    df["economy_size"] = df["gdp_usd"].apply(categorize)

    # New Column 3: Timestamp
    df["loaded_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Save as Parquet
    path = "transformed/gdp_clean.parquet"
    df.to_parquet(path, index=False)
    logging.info(f"GDP transformed and saved to {path} — {len(df)} rows")
    print(f"✅ GDP data transformed — {len(df)} rows saved to {path}")

# ── TRANSFORM POPULATION DATA ──────────────────
def transform_population():
    logging.info("Transforming Population data...")

    # Read raw file from landing zone
    df = pd.read_csv("landing_zone/population_raw.csv")

    # Rename columns to be cleaner
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # Keep only recent years (2000 onwards)
    df = df[df["year"] >= 2000]

    # Remove nulls
    df = df.dropna()

    # New Column 1: Population in Millions
    df["population_millions"] = (df["value"] / 1_000_000).round(4)

    # New Column 2: Timestamp
    df["loaded_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Save as Parquet
    path = "transformed/population_clean.parquet"
    df.to_parquet(path, index=False)
    logging.info(f"Population transformed and saved to {path} — {len(df)} rows")
    print(f"✅ Population data transformed — {len(df)} rows saved to {path}")

# ── RUN BOTH ───────────────────────────────────
if __name__ == "__main__":
    print("Starting transformations...")
    transform_gdp()
    transform_population()
    print("✅ All data transformed and saved to transformed folder!")