import requests
import pandas as pd
from google.cloud import storage
from google.auth import exceptions

# Define the SCB API URL
url = "https://api.scb.se/OV0104/v1/doris/sv/ssd/NV/NV0116/NV0116M/AITab01"

# Your query for Andel
query_andel = {
    "query": [
        {
            "code": "Andamal",  # Section (formerly Andamal)
            "selection": {
                "filter": "item",
                "values": ["A01", "A02", "A05"]
            }
        },
        {
            "code": "Redovisningsgrupp",
            "selection": {
                "filter": "item",
                "values": [
                    "Tot250", "10-49", "50-249", "250-", 
                    "TotSNI", "10-33", "35-39", "41-43", "45-47", "49-53", 
                    "55-56", "58-63", "68",  "IKT", "SE", "RIKS1", "RIKS2", 
                    "RIKS3", "RIKS4", "RIKS5", "RIKS6", "RIKS7", "RIKS8"
                ]
            }
        },
        {
            "code": "ContentsCode",
            "selection": {
                "filter": "item",
                "values": ["0000034S"]  # Andel
            }
        },
        {
            "code": "Tid",  # Year (formerly Tid)
            "selection": {
                "filter": "item",
                "values": ["2021", "2023", "2024"]
            }
        }
    ],
    "response": {
        "format": "json"
    }
}

# Function to fetch and process data
def fetch_data(query):
    response = requests.post(url, json=query)
    response.raise_for_status()  # Raise an error for bad responses
    data = response.json()

    records = []
    for obs in data['data']:
        record = {var['code']: val for var, val in zip(data['columns'], obs['key'])}
        # Extracting 'value' corresponding to '0000034S' (andel, procent)
        record['value_andel'] = obs['values'][0]  # Use value_andel as returned by the API
        records.append(record)

    df = pd.DataFrame(records)
    return df

# Function to clean the 'value_andel' column and ensure numeric values
def clean_value_andel(value):
    try:
        # Try converting the value to a float
        return float(value)
    except ValueError:
        # Return None for invalid (non-numeric) values
        return None

# Fetch and process the Andel data
df_andel = fetch_data(query_andel)

# Clean the data
df_andel['value_andel'] = df_andel['value_andel'].apply(clean_value_andel)

# Split 'Redovisningsgrupp' into correct columns
df_andel['Company Size'] = df_andel['Redovisningsgrupp'].apply(
    lambda x: x if x in ["Tot250", "10-49", "50-249", "250-"] else None)
df_andel['Size Classification'] = df_andel['Redovisningsgrupp'].apply(
    lambda x: x if x in ["TotSNI", "10-33", "35-39", "41-43", "45-47", "49-53", 
                         "55-56", "58-63", "68", "69-82+95.1exkl.75", "69-75, 77-82, 95.1", "IKT"] else None)
df_andel['Region'] = df_andel['Redovisningsgrupp'].apply(
    lambda x: x if x in ["SE", "RIKS1", "RIKS2", "RIKS3", "RIKS4", "RIKS5", 
                         "RIKS6", "RIKS7", "RIKS8"] else None)

# Rename columns to English
df_andel = df_andel.rename(columns={
    'Andamal': 'Section',
    'Tid': 'Year',
    'Redovisningsgrupp': 'Original Classification',  # Keep original classification
    'Företagsstorlek': 'Company Size',
    'Område': 'Region',
    'Size Classification': 'Classification'  # Updated classification name
})

# Save processed data to CSV
df_andel.to_csv('data.csv', index=False)

# Upload CSV to Google Cloud Storage
bucket_name = 'zoomcamp-data-bucket'
destination_blob_name = 'data.csv'

try:
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename('data.csv')
    print("✅ Data uploaded to GCS.")
except exceptions.DefaultCredentialsError:
    print("❌ Error: Could not authenticate with Google Cloud.")

# Additional code to generate and upload labels.csv if not yet created
url_labels = 'https://api.scb.se/OV0104/v1/doris/sv/ssd/NV/NV0116/NV0116M/AITab01'
response_labels = requests.get(url_labels, params={'lang': 'en'})

if response_labels.status_code == 200:
    try:
        data_labels = response_labels.json()
        print("Successfully fetched metadata for labels")

        labels = {}
        for variable in data_labels.get('variables', []):
            if 'values' in variable:
                for i, value in enumerate(variable['values']):
                    code = value  # For example, "A01", "Tot250"
                    translation = variable.get('valueTexts', [])[i]  # This will match the translation
                    labels[code] = translation

        # Create the labels CSV file
        labels_filename = 'labels.csv'
        with open(labels_filename, 'w', encoding='utf-8-sig') as f:
            f.write("ID,Label\n")
            for code, label in labels.items():
                f.write(f"{code},{label}\n")

        # Upload the labels CSV file to Google Cloud Storage
        blob_labels = bucket.blob(labels_filename)
        blob_labels.upload_from_filename(labels_filename)
        print(f"Labels file uploaded to GCS: {labels_filename}")

    except json.decoder.JSONDecodeError as e:
        print("Failed to parse JSON response:", e)

else:
    print(f"Failed to fetch metadata for labels. Status code: {response_labels.status_code}")
