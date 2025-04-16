# zoomcamp-project
End-to-end data pipeline 

## Project Overview
The Zoomcamp Project implements an end-to-end data pipeline to analyze how companies in Sweden adopt artificial intelligence technologies, specifically focusing on the adoption of AI software or systems across company size, region, and industry.
## Problem Statement
The aim of this project is to build a data pipeline that fetches AI adoption data from Statistics Sweden (SCB), processes it, stores it in a data warehouse, and then visualizes the data in an interactive dashboard. The final goal is to present insights into how AI adoption varies across different sectors and years (2021-2024).
## Overview of Solution
This solution leverages a modern data engineering stack to accomplish the task:

- Data ingestion: Data is fetched dynamically from SCB’s RESTful API using Python scripts inside a Docker container.
- Data storage: The data is uploaded to Google Cloud Storage and processed with DBT for transformation.
- Orchestration: The workflow is orchestrated by Prefect to automate the ingestion and transformation processes.
- Data warehousing: The data is stored in BigQuery for scalable querying and analysis.
- Dashboard: An interactive dashboard in Looker Studio provides insights into AI adoption in Swedish companies.

### Tech Stack:
- Docker & Python
- Google Cloud Storage (GCS)
- BigQuery (data warehouse)
- dbt (transformations)
- Looker Studio or Power BI (dashboard)
- Prefect (workflow orchestration)
- Terraform (for cloud infrastructure)


# Step-by-step Guide

This guide will walk you through setting up and running the zoomcamp-project end-to-end data pipeline.

## Prerequisites



### Install Tools
Before starting, ensure that you have the following tools below installed,
- **Install a code editor** (VS Code, or any code editor of your choice).
  - [Download VS Code here](https://code.visualstudio.com/).
- **Install Docker** and **Docker Compose**.
  - [Install Docker here](https://www.docker.com/get-started).
- **Install Google Cloud SDK** (for GCP authentication).
  - [Install the Google Cloud SDK here](https://cloud.google.com/sdk/docs/install).
- **Install Terraform** (for provisioning infrastructure).
  - [Install Terraform here](https://www.terraform.io/downloads).
- **Install dbt** (for data transformations).
  - You can install dbt with `pip` (Python package manager). Since im using BigQuery i install the following:
    ```bash
    pip install dbt-bigquery
    ```
  - For detailed installation instructions, refer to the official [dbt installation guide](https://docs.getdbt.com/docs/installation).
  - **Install Prefect** (workflow orchestration tool)
  - Install with pip:
    ```bash
    pip install prefect
    ```


## Google Cloud Setup

1. **Create a Google Cloud Account**  
   Sign up at [Google Cloud](https://cloud.google.com/) to get started.

2. **Generate and Configure Service Account Credentials**  
   - Create a service account and generate a **JSON key** [here](https://console.cloud.google.com/iam-admin/serviceaccounts).
   - Set the credentials environment variable:

   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/credentials-file.json"
   ```

## Terraform Setup

1. **Initialize Terraform**, **Plan** the Infrastructure Deployment, and **Apply** the Terraform Configuration to create the GCS bucket and BigQuery dataset in your Google Cloud account:

## Files in the `terraform/` folder:´
 - `main.tf`         Defines the GCS bucket and BigQuery dataset 
 - `variables.tf`    Declares input variables used by Terraform
 - `terraform.tfvars`  Contains actual values like project ID, region, etc.
 - `outputs.tf`        Displays output values after resources are created 

 Run command:

  ```bash
  terraform init
  terraform plan
  terraform apply
  ```

Required permissions: Ensure the service account you're using has these IAM roles:
  - Storage Admin
  - BigQuery Admin

Assign roles via the IAM Console.

## Architecture
The architecture diagram below shows the high-level architecture of the data pipeline:

![Architecture Diagram](images/Architecture.png)


## Steps for the Pipeline
### 1. Provision Infrastructure with Terraform  
Terraform is used to automatically create:
- A Google Cloud Storage (GCS) bucket for storing raw data
- A BigQuery dataset for analytics and transformation
This is done by the command showed in Terraform setup above. 

### 2. SCB (CSV Data)
 - Source: Data is fetched from the official [SCB Statistics Database](https://www.statistikdatabasen.scb.se/pxweb/sv/ssd/), the official Swedish statistics bureau.
 - API Ingestion: The data is fetched automatically via a Python script using a structured JSON POST request to SCB’s official API ([PxWeb API 2.0](https://www.scb.se/vara-tjanster/oppna-data/pxwebapi/pxwebapi-2.0)).
 - Frequency: Although the underlying dataset is updated annually, the pipeline is scheduled to run monthly to simulate real-time ingestion and demonstrate workflow orchestration best practices.

### 3. Docker (Python ETL)
- Create Docker Image: The Docker container runs Python scripts to:
- Ingestion: Fetches data from the SCB API and saves it as CSV files.
- Data Upload: Uploads the CSV data to Google Cloud Storage (GCS) for storage.
- Data Loading to BigQuery: After the data is uploaded to GCS, the Python script loads the data from GCS into BigQuery.

**Note**: The Docker image used for this project is hosted on **[Docker Hub](https://hub.docker.com/)**. 

Create and run Docker Container:
  ```bash
docker build -t <image-name> .
docker run -d --name <container-name> <image-name>
  ```

### 4. Google Cloude Storage (Data Lake)
- Purpose: GCS is used as a data lake to store the raw CSV data before moving it to BigQuery.

### 5. BigQuery (Data Warehouse)

The raw CSV file stored in Google Cloud Storage is batch-loaded into BigQuery using a Python script.
BigQuery acts as the central data warehouse, enabling scalable querying and downstream transformations with dbt.

### 6. dbt (Transformations)
- Transformation: The data in BigQuery is transformed using dbt to apply necessary data preparation for analysis.

#### Steps:
- Models: Created models to translate the Section, Classification, and Region columns.
- Translation: Translated these columns using a join on the label table, while keeping the Company Size column unchanged.
- Execution: Run dbt to execute the transformations, creating the model.

### 7. [Dashboard](https://lookerstudio.google.com/reporting/4285d0bb-c7ef-44e3-abce-9220b4bcec80) (Looker Studio)
Visualization: The transformed data is visualized in Looker Studio, displaying insights into AI adoption across sectors and years. This is done via a connection to BigQuery database. 

#### Steps Taken:
- Connecting BigQuery Database: I connected the BigQuery database, where the transformed data is stored, to Looker Studio. This enables seamless visualization of AI adoption data.

![Dashboard](images/Dashboard.png)

### 8. Prefect: Workflow Orchestration
This project uses [Prefect](https://www.prefect.io/) to automate and orchestrate the data pipeline. Prefect handles the scheduling and execution of the ingestion and transformation tasks, ensuring that the AI adoption data is processed and updated regularly without manual intervention. Although the SCB dataset updates annually, we’ve configured the workflow to run monthly to demonstrate automation best practices and efficient orchestration design.

Prefect Tasks:
- Docker Container: Fetches data from the SCB API, processes it, and uploads to GCS.
- DBT Transformations: Runs after the Docker task to clean and process data for BigQuery.
- Scheduling: Prefect’s Interval Schedule runs the flow every 30 days, keeping data updated despite annual dataset updates.
- Flow Execution: The flow orchestrates the tasks to automate data ingestion, processing, and reporting.
- Deployment: The flow is deployed to Prefect Cloud, triggering automatically on the set schedule for seamless processing.

### 9. Upload to GitHub

Upload the following files to a GitHub repository to make it accessible for Prefect:

- **DBT SQL files** for transformations
- **Python scripts** for ingestion and processing
- **Dockerfile** for building the Docker image
- **requirements.txt** listing all project dependencies
    
  ```bash
        git add .
        git commit -m
        git push origin main
  ```

# Conclusion

This project implements a full data pipeline that ingests data from SCB, processes it, stores it in Google Cloud, and visualizes it through Looker Studio. Prefect is used to automate and orchestrate the entire process, while Terraform provisions the cloud infrastructure.