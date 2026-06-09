# Use Python 3.11 as base image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements file first
COPY requirements.txt .

# Install all libraries
RUN pip install -r requirements.txt

# Copy all project files
COPY . .

# Create necessary folders
RUN mkdir -p landing_zone transformed logs

# Run ingest and transform first, then start dashboard
CMD python ingest.py && python transform.py && streamlit run dashboard.py --server.port=8501 --server.address=0.0.0.0