import requests
import json
from google.cloud import storage

# Configuration for Google Cloud Storage
bucket_name = 'zoomcamp-data-bucket'
storage_client = storage.Client()
bucket = storage_client.get_bucket(bucket_name)

# SCB API endpoint (The endpoint remains the same)
url = 'https://api.scb.se/OV0104/v1/doris/sv/ssd/NV/NV0116/NV0116M/AITab01'

# SCB API call to fetch metadata (labels and region data) in English
response = requests.get(url, params={'lang': 'en'})

# Log the response content for debugging
print("Response Status Code:", response.status_code)
print("Response Content:", response.text)

if response.status_code == 200:
    try:
        data = response.json()
        print("Successfully fetched metadata")

        # Prepare the labels and codes from the response
        labels = {}

        # Extracting the 'Andamal' and 'Redovisningsgrupp' sections from the API response
        for variable in data.get('variables', []):
            if 'values' in variable:
                for i, value in enumerate(variable['values']):
                    code = value  # For example, "A01", "Tot250"
                    translation = variable.get('valueTexts', [])[i]  # This will match the translation
                    labels[code] = translation  # Map the code to the translation

        # Create the labels CSV file
        labels_filename = 'labels.csv'
        with open(labels_filename, 'w', encoding='utf-8-sig') as f:  # Use utf-8-sig to handle special characters
            f.write("ID,Label\n")
            for code, label in labels.items():
                f.write(f"{code},{label}\n")

        # Upload the CSV file to Google Cloud Storage
        blob_labels = bucket.blob(labels_filename)
        blob_labels.upload_from_filename(labels_filename)
        print(f"Labels file uploaded to GCS: {labels_filename}")

    except json.decoder.JSONDecodeError as e:
        print("Failed to parse JSON response:", e)

else:
    print(f"Failed to fetch metadata from SCB API. Status code: {response.status_code}")
