# analytics.py
# This file runs 5 analytical queries on the cleaned parquet files

import duckdb
import pandas as pd

# Connect to DuckDB
conn = duckdb.connect()

print("=" * 50)
print("📊 ANALYTICS REPORT")
print("=" * 50)

# ── QUERY 1: Top 10 Largest Economies ──────────
print("\n🏆 Query 1: Top 10 Largest Economies by GDP")
q1 = conn.execute("""
    SELECT 
        country_name,
        gdp_trillion,
        economy_size
    FROM read_parquet('transformed/gdp_clean.parquet')
    ORDER BY gdp_usd DESC
    LIMIT 10
""").df()
print(q1.to_string(index=False))

# ── QUERY 2: Count of Economies by Size ────────
print("\n📊 Query 2: Count of Countries by Economy Size")
q2 = conn.execute("""
    SELECT 
        economy_size,
        COUNT(*) as country_count
    FROM read_parquet('transformed/gdp_clean.parquet')
    GROUP BY economy_size
    ORDER BY country_count DESC
""").df()
print(q2.to_string(index=False))

# ── QUERY 3: Average GDP by Economy Size ───────
print("\n💰 Query 3: Average GDP (Trillion) by Economy Size")
q3 = conn.execute("""
    SELECT 
        economy_size,
        ROUND(AVG(gdp_trillion), 4) as avg_gdp_trillion
    FROM read_parquet('transformed/gdp_clean.parquet')
    GROUP BY economy_size
    ORDER BY avg_gdp_trillion DESC
""").df()
print(q3.to_string(index=False))

# ── QUERY 4: Top 10 Most Populous Countries ────
print("\n👥 Query 4: Top 10 Most Populous Countries (Latest Year)")
q4 = conn.execute("""
    SELECT 
        country_name,
        year,
        population_millions
    FROM read_parquet('transformed/population_clean.parquet')
    WHERE year = (SELECT MAX(year) FROM read_parquet('transformed/population_clean.parquet'))
    ORDER BY population_millions DESC
    LIMIT 10
""").df()
print(q4.to_string(index=False))

# ── QUERY 5: Population Growth Trend ───────────
print("\n📈 Query 5: World Population Growth by Year (2000-2020)")
q5 = conn.execute("""
    SELECT 
        year,
        ROUND(SUM(population_millions), 2) as total_population_millions
    FROM read_parquet('transformed/population_clean.parquet')
    WHERE country_name = 'World'
    GROUP BY year
    ORDER BY year
""").df()
print(q5.to_string(index=False))

print("\n" + "=" * 50)
print("✅ Analytics complete!")
conn.close()