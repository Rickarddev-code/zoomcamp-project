# Use official lightweight Python image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files into the container
COPY . .

# Copy the Google Cloud service account credentials file
COPY zoomcamp-456820-3b008153d0b0.json /app/zoomcamp-456820-3b008153d0b0.json

# Set the environment variable for Google Cloud authentication
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/zoomcamp-456820-3b008153d0b0.json"

# Copy the existing ingest script and the new labels ingestion script
COPY ingest_from_scb_api.py /app/ingest_from_scb_api.py
COPY ingest_from_scb_labels_api.py /app/ingest_from_scb_labels_api.py
COPY load_to_bigquery.py /app/load_to_bigquery.py 

# Run ingest_from_scb_api.py first, then ingest_from_scb_labels_api.py, and then load_to_bigquery.py
CMD ["sh", "-c", "python ingest_from_scb_api.py && python ingest_from_scb_labels_api.py && python load_to_bigquery.py"]
