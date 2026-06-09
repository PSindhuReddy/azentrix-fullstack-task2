# Mini Data Lakehouse with Analytics Dashboard — Task 2

## What This Project Does
A layered data architecture that:
- Ingests data from 2 different sources (World Bank API + Population CSV)
- Stores raw data in a landing zone
- Transforms and saves cleaned data as Parquet files
- Runs 5 meaningful analytical queries
- Presents results in a Streamlit dashboard
- Fully containerized using Docker Compose

## Project Structure
azentrix-fullstack-task2/
├── ingest.py            → Downloads raw data from 2 sources
├── transform.py         → Cleans and saves Parquet files
├── analytics.py         → Runs 5 SQL queries
├── dashboard.py         → Visual Streamlit dashboard
├── Dockerfile           → Docker image instructions
├── docker-compose.yml   → Runs everything together
├── requirements.txt     → Required libraries
├── landing_zone/        → Raw CSV files (landing zone)
│   ├── gdp_raw.csv
│   └── population_raw.csv
├── transformed/         → Cleaned Parquet files
│   ├── gdp_clean.parquet
│   └── population_clean.parquet
└── logs/                → Log files
├── ingest.log
└── transform.log
## Data Sources
1. **World Bank API** — GDP data for all countries
   - URL: https://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.CD
2. **World Population CSV** — Population data by country
   - URL: https://raw.githubusercontent.com/datasets/population/master/data/population.csv

## Data Model
gdp_clean.parquet
├── country_name    → Name of country
├── country_code    → ISO country code
├── year            → Year of data
├── gdp_usd         → GDP in USD
├── gdp_trillion    → GDP in Trillions (derived)
├── economy_size    → Large/Medium/Small (derived)
└── loaded_at       → Timestamp of load
population_clean.parquet
├── country_name         → Name of country
├── country_code         → ISO country code
├── year                 → Year of data
├── value                → Raw population value
├── population_millions  → Population in Millions (derived)
└── loaded_at            → Timestamp of load
## Analytical Queries
1. Top 10 Largest Economies by GDP
2. Count of Countries by Economy Size
3. Average GDP by Economy Size
4. Top 10 Most Populous Countries (2024)
5. World Population Growth (2000-2024)

## Setup Instructions

### Option 1: Run Locally
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/azentrix-fullstack-task2
cd azentrix-fullstack-task2

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

# Install libraries
pip install -r requirements.txt

# Run ingestion
python ingest.py

# Run transformation
python transform.py

# Run dashboard
streamlit run dashboard.py
```

### Option 2: Run with Docker
```bash
# Make sure Docker Desktop is installed
docker-compose up --build
```
Then open your browser at http://localhost:8501

## Tools Used
- Python 3.11
- Pandas — data manipulation
- DuckDB — analytical queries
- Streamlit — dashboard
- PyArrow — Parquet files
- Docker — containerization