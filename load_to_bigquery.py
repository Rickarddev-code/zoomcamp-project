from google.cloud import bigquery
from google.cloud import storage
import pandas as pd

# Initialize BigQuery and Storage clients
client = bigquery.Client()
storage_client = storage.Client()

# Define GCS bucket and file paths
bucket_name = 'zoomcamp-data-bucket'
data_file_name = 'data.csv'  # Main data file
labels_file_name = 'labels.csv'  # Labels data file
gcs_data_uri = f"gs://{bucket_name}/{data_file_name}"
gcs_labels_uri = f"gs://{bucket_name}/{labels_file_name}"

# Define BigQuery dataset and table references
project_id = 'zoomcamp-456820'
dataset_id = 'zoomcamp_ai'
main_table_id = 'ai_adoption'
labels_table_id = 'labels_table'

# Load main data (data.csv) to BigQuery
main_table_ref = f"{project_id}.{dataset_id}.{main_table_id}"

# Updated schema to account for all 7 columns
main_job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.CSV,
    skip_leading_rows=1,
    autodetect=False,  # Manually define the schema
    schema=[  # Updated schema for all columns including 'Original Classification'
        bigquery.SchemaField("Section", "STRING"),  # 'Andamal' changed to 'Section'
        bigquery.SchemaField("Original Classification", "STRING"),  # New column 'Original Classification'
        bigquery.SchemaField("Year", "STRING"),  # 'Tid' changed to 'Year'
        bigquery.SchemaField("value_andel", "FLOAT64"),
        bigquery.SchemaField("Company Size", "STRING"),  # 'Företagsstorlek' changed to 'Company Size'
        bigquery.SchemaField("Classification", "STRING"),  # 'SNI' changed to 'Classification'
        bigquery.SchemaField("Region", "STRING"),  # 'Område' changed to 'Region'
    ]
)

# Load the main data from GCS to BigQuery
load_job_main = client.load_table_from_uri(
    gcs_data_uri,
    main_table_ref,
    job_config=main_job_config
)
load_job_main.result()  # Wait for the load job to finish

# Confirm that the main table data is loaded
destination_main_table = client.get_table(main_table_ref)
print(f"✅ Main table {main_table_ref} has {destination_main_table.num_rows} rows.")

# Load labels data (labels.csv) to BigQuery
labels_table_ref = f"{project_id}.{dataset_id}.{labels_table_id}"
labels_job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.CSV,
    skip_leading_rows=1,
    autodetect=True,  # Let BigQuery auto-detect the labels schema
)

# Load the labels data from GCS to BigQuery
load_job_labels = client.load_table_from_uri(
    gcs_labels_uri,
    labels_table_ref,
    job_config=labels_job_config
)
load_job_labels.result()  # Wait for the load job to finish

# Confirm that the labels data is loaded
destination_labels_table = client.get_table(labels_table_ref)
print(f"✅ Labels table {labels_table_ref} has {destination_labels_table.num_rows} rows.")
