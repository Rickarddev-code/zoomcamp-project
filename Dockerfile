# Use official lightweight Python image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code and data into the container
COPY . .

# Ensure data.csv is copied into the container
COPY data/data.csv /app/data.csv

# Copy the Google Cloud service account credentials file into the container
COPY zoomcamp-456820-3b008153d0b0.json /app/zoomcamp-456820-3b008153d0b0.json

# Set the environment variable for Google Cloud Authentication
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/zoomcamp-456820-3b008153d0b0.json"

# Run the script when the container starts
CMD ["python", "ingest_data.py"]
