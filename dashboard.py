# dashboard.py
# This file creates a visual dashboard using Streamlit

import streamlit as st
import duckdb
import pandas as pd

# ── PAGE SETUP ─────────────────────────────────
st.set_page_config(
    page_title="Data Lakehouse Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Data Lakehouse Analytics Dashboard")
st.markdown("**Data Sources:** World Bank GDP API + World Population CSV")
st.divider()

# ── CONNECT TO DUCKDB ──────────────────────────
conn = duckdb.connect()

# ── QUERY 1: Top 10 Largest Economies ──────────
st.subheader("🏆 Top 10 Largest Economies by GDP")
q1 = conn.execute("""
    SELECT 
        country_name,
        gdp_trillion,
        economy_size
    FROM read_parquet('transformed/gdp_clean.parquet')
    WHERE country_name NOT IN ('World', 'High income', 'OECD members', 
        'Low & middle income', 'Middle income', 'IBRD only',
        'IDA & IBRD total', 'Post-demographic dividend',
        'Early-demographic dividend', 'Late-demographic dividend',
        'North America', 'East Asia & Pacific')
    ORDER BY gdp_trillion DESC
    LIMIT 10
""").df()
st.bar_chart(q1.set_index("country_name")["gdp_trillion"])
st.dataframe(q1, width='stretch')
st.divider()

# ── QUERY 2: Economy Size Distribution ─────────
st.subheader("📊 Countries by Economy Size")
q2 = conn.execute("""
    SELECT 
        economy_size,
        COUNT(*) as country_count
    FROM read_parquet('transformed/gdp_clean.parquet')
    GROUP BY economy_size
    ORDER BY country_count DESC
""").df()
st.bar_chart(q2.set_index("economy_size")["country_count"])
st.dataframe(q2, width='stretch')
st.divider()

# ── QUERY 3: Average GDP by Economy Size ───────
st.subheader("💰 Average GDP (Trillion) by Economy Size")
q3 = conn.execute("""
    SELECT 
        economy_size,
        ROUND(AVG(gdp_trillion), 4) as avg_gdp_trillion
    FROM read_parquet('transformed/gdp_clean.parquet')
    GROUP BY economy_size
    ORDER BY avg_gdp_trillion DESC
""").df()
st.bar_chart(q3.set_index("economy_size")["avg_gdp_trillion"])
st.dataframe(q3, width='stretch')
st.divider()

# ── QUERY 4: Top 10 Most Populous Countries ────
st.subheader("👥 Top 10 Most Populous Countries (2024)")
q4 = conn.execute("""
    SELECT 
        country_name,
        year,
        population_millions
    FROM read_parquet('transformed/population_clean.parquet')
    WHERE year = (SELECT MAX(year) FROM read_parquet('transformed/population_clean.parquet'))
    AND country_name NOT IN ('World', 'IDA & IBRD total', 'Low & middle income',
        'Middle income', 'IBRD only', 'Early-demographic dividend',
        'Lower middle income', 'Upper middle income', 'East Asia & Pacific',
        'Late-demographic dividend')
    ORDER BY population_millions DESC
    LIMIT 10
""").df()
st.bar_chart(q4.set_index("country_name")["population_millions"])
st.dataframe(q4, width='stretch')
st.divider()

# ── QUERY 5: World Population Growth ───────────
st.subheader("📈 World Population Growth (2000-2024)")
q5 = conn.execute("""
    SELECT 
        year,
        ROUND(SUM(population_millions), 2) as total_population_millions
    FROM read_parquet('transformed/population_clean.parquet')
    WHERE country_name = 'World'
    GROUP BY year
    ORDER BY year
""").df()
st.line_chart(q5.set_index("year")["total_population_millions"])
st.dataframe(q5, width='stretch')

st.divider()
st.markdown("Built with ❤️ using Python, DuckDB, and Streamlit")

conn.close()