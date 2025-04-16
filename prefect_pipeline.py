from prefect import task, flow
from datetime import timedelta
import subprocess

# Define the task to build and run Docker container
@task
def build_and_run_docker():
    # Build Docker image
    subprocess.run(["docker", "build", "-t", "zoomcamp-image", "."], check=True)

    # Run Docker container
    subprocess.run(["docker", "run", "-d", "--name", "zoomcamp-container", "zoomcamp-image"], check=True)

# Define the task to run DBT transformations
@task
def run_dbt():
    # Run DBT transformations
    subprocess.run(["dbt", "run", "--project-dir", "zoomcamp_dbt"], check=True)

# Create the flow (no schedule applied directly here)
@flow
def build_and_run_pipeline():
    # First, build and run the Docker container
    docker_task = build_and_run_docker()
    
    # Once Docker task is complete, run the DBT transformations
    run_dbt(upstream_tasks=[docker_task])

# Deploy the flow and schedule it to run every 30 days
if __name__ == "__main__":
    build_and_run_pipeline.serve(
        name="build-and-run-pipeline-deployment",
        cron="0 0 1 * *",  # Every 30 days (adjust for exact time)
        tags=["AI-Pipeline", "Scheduled"],
        description="Build and run Docker container, then execute DBT transformations.",
    )
