import os
import pandas as pd
from google.cloud import storage
from google.auth import exceptions

# Verify that the CSV file exists
if not os.path.exists('data.csv'):
    print("Error: data.csv file not found!")
else:
    # Load the CSV file that contains the raw AI usage data
    df = pd.read_csv("data/data.csv", encoding="ISO-8859-1", delimiter="\t", on_bad_lines='skip')


    # Clean the data (optional but useful for missing values)
    df.replace("..", pd.NA, inplace=True)

    # Print a quick preview just to verify it worked
    print("Preview of the dataset:")
    print(df.head())

    # Google Cloud Storage configuration
    bucket_name = 'zoomcamp-data-bucket'  # Replace with your GCS bucket name
    destination_blob_name = 'data.csv'    # The name you want the file to have in GCS

    # Initialize a GCS client
    try:
        storage_client = storage.Client()
        storage_client.get_bucket(bucket_name)  # Testing the connection to GCS
        print("Google Cloud credentials and connection are working.")
    except exceptions.DefaultCredentialsError:
        print("Error: Could not authenticate with Google Cloud. Please check your credentials.")
        exit(1)

    # Get the bucket
    bucket = storage_client.get_bucket(bucket_name)

    # Upload the CSV file to GCS
    try:
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename('data.csv')
        print(f"File {destination_blob_name} uploaded to {bucket_name}.")
    except Exception as e:
        print(f"An error occurred during upload: {e}")

    # Verify the file exists in GCS
    blob = bucket.blob(destination_blob_name)
    if blob.exists():
        print(f"File {destination_blob_name} exists in {bucket_name}.")
    else:
        print(f"File {destination_blob_name} was not uploaded.")