provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_storage_bucket" "data_lake_bucket" {
  name     = var.bucket_name
  location = var.region
  force_destroy = true

  uniform_bucket_level_access = true
}

resource "google_bigquery_dataset" "ai_dataset" {
  dataset_id = var.dataset_id
  location   = var.region
}
