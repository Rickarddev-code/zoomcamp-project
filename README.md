# zoomcamp-project
End-to-end data pipeline 

## Project Overview

## Problem Statement

## Overview of Solution

# Zoomcamp Project – AI Adoption in Swedish Companies

This project implements an end-to-end data pipeline to analyze how companies in Sweden adopt artificial intelligence technologies. 

The dataset is sourced from Statistics Sweden (SCB), focusing on the usage of AI-based software or systems across company size, region, and industry from 2021 to 2024.

The goal is to create a reproducible pipeline using modern data engineering tools, with the final insights visualized in an interactive dashboard.

**Tech stack:**
- Docker & Python
- Google Cloud Storage (GCS)
- BigQuery (data warehouse)
- dbt (transformations)
- Looker Studio  or Power BI (dashboard)





## Step-by-step Guide

This guide is designed to help you set up and run the zoomcamp-project end-to-end data pipeline, even if you are new to the tools and technologies involved. Each step is explained in a way that ensures you can follow along without prior knowledge of data engineering.

### Prerequisites

Before starting, make sure you have a code editor installed. If you don’t already have a favorite, [Visual Studio Code (VS Code)](https://code.visualstudio.com/) is a commonly used option that I have chosen for this project. However, you can use any editor you’re comfortable with.

# Install Tools

- **Install a code editor** (VS Code, or any code editor of your choice).
  - [Download VS Code here](https://code.visualstudio.com/).
- **Install Docker** and **Docker Compose**.
  - [Install Docker here](https://www.docker.com/get-started).
- **Install Google Cloud SDK** (for GCP authentication).
  - [Install the Google Cloud SDK here](https://cloud.google.com/sdk/docs/install).
- **Install Terraform** (for provisioning infrastructure).
  - [Install Terraform here](https://www.terraform.io/downloads).
- **Install dbt** (for data transformations).
  - You can install dbt with `pip` (Python package manager):
    ```bash
    pip install dbt
    ```
  - For detailed installation instructions, refer to the official [dbt installation guide](https://docs.getdbt.com/docs/installation).

# Google Cloud Setup


1. **Create a Google Cloud Account**  
   Sign up at [Google Cloud](https://cloud.google.com/) to get started.

2. **Set Up Google Cloud Storage (GCS) and BigQuery**  
   Follow these guides to create your resources:
   - [Create a Cloud Storage Bucket](https://cloud.google.com/storage/docs/creating-buckets) for storing raw data.
   - [Create a BigQuery Dataset](https://cloud.google.com/bigquery/docs/datasets) for querying data.

3. **Generate and Configure Service Account Credentials**  
   - Create a service account and generate a **JSON key** [here](https://console.cloud.google.com/iam-admin/serviceaccounts).
   - Set the credentials environment variable:

   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/credentials-file.json"

# Terraform Setup

1. **Initialize Terraform**, **Plan** the Infrastructure Deployment, and **Apply** the Terraform Configuration to create the GCS bucket and BigQuery dataset in your Google Cloud account:

   ```bash
   terraform init
   terraform plan
   terraform apply

## Architecture
Now that we have set up all the necessary tools and accounts, let's move on to the architecture process. The diagram below illustrates the high-level architecture of the end-to-end data pipeline implemented in this project. Each component plays a specific role in the process of ingesting, transforming, and visualizing SCB-provided CSV data. 

![Architecture Diagram](images/Architecture.png)

1. SCB (CSV Data)
 - Source: Data is fetched from the official [SCB Statistics Database](https://www.statistikdatabasen.scb.se/pxweb/sv/ssd/). The source data comes from the official Swedish statistics bureau (SCB).
 - Dataset: The dataset contains information on AI adoption in Swedish companies (2021, 2022 & 2024), provided in CSV format.
 - Download: We manually downloaded the CSV file for this project. In a real scenario, we’d automate this with Airflow or similar tools to fetch data periodically.
 
2. Docker (Python ETL)
- Create Dockerfile: You can find the Dockerfile for the Python ETL process in the repository under the Dockerfile
- Create Docker Image: 
    ```bash
    docker build -t <pick a name for image> .
- Run Docker Container: 
     ```bash
    docker run -d --name <pick a name for containter> <name of image>
- Python Script: The Python script inside the container will:
 - Read the downloaded SCB CSV data.
 - Upload the data to Google Cloud Storage (GCS).

3. GCS (Data Lake)
Google Cloud Storage is used as a data lake to store raw data files. This allows for scalable and cost-effective storage before loading data into the warehouse.

4. BigQuery (Data Warehouse)
The raw CSV data in GCS is loaded into BigQuery using batch loading jobs. BigQuery serves as the central data warehouse for querying and analytics.

5. dbt (Transformations)
Data Build Tool (dbt) is used to model and transform the raw data into clean, analytics-ready tables within BigQuery. dbt allows for version control, modular SQL, and testing.

6. Dashboard (Looker)
A Looker Studio dashboard is connected to the transformed tables in BigQuery. It provides interactive visualizations, including time-based trends and categorical breakdowns.

7. Terraform
Terraform is used to provision the required cloud infrastructure on GCP. It automates the creation of:
   The GCS bucket used as the data lake
   The BigQuery dataset used for warehousing and transformation




### Part 1: Setting Up Docker
1. Install Docker Desktop.
2. In your project directory, create a `Dockerfile` for your environment setup.

### Part 2: Using Terraform
1. Configure your GCP credentials and initialize Terraform.
2. Apply the Terraform configuration to provision the GCS bucket and BigQuery dataset.

### Part 3: Python ETL Pipeline
1. Create a Python script to download the data from SCB (or simulate this for the project).
2. Use the Docker container to run the Python script to upload the data into GCS.

### Part 4: dbt Transformations
1. Set up dbt to connect to your BigQuery dataset.
2. Define models and run dbt to transform the raw data into usable tables for analysis.

### Part 5: Visualization
1. Use Looker Studio or Power BI to connect to BigQuery and visualize the data.