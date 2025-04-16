variable "project_id" {
  type        = string
  description = "GCP project ID"
}

variable "region" {
  type        = string
  default     = "EU"
  description = "GCP region (multi-region EU)"
}

variable "bucket_name" {
  type        = string
  default     = "zoomcamp-data-bucket"
  description = "Name of the GCS bucket to be created"
}

variable "dataset_id" {
  type        = string
  default     = "zoomcamp_ai"
  description = "BigQuery dataset ID"
}
