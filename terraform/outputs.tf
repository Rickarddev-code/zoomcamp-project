output "bucket_name" {
  value = google_storage_bucket.data_lake_bucket.name
}

output "bigquery_dataset" {
  value = google_bigquery_dataset.ai_dataset.dataset_id
}
