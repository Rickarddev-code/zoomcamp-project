from prefect import task, flow
from prefect_github import GitRepository
from datetime import timedelta
import subprocess

# Define the task to build and run Docker container
@task
def build_and_run_docker():
    subprocess.run(["docker", "build", "-t", "zoomcamp-image", "."], check=True)
    subprocess.run(["docker", "run", "-d", "--name", "zoomcamp-container", "zoomcamp-image"], check=True)

# Define the task to run DBT transformations
@task
def run_dbt():
    subprocess.run(["dbt", "run", "--project-dir", "zoomcamp_dbt"], check=True)

# Define the flow that will be scheduled and triggered from GitHub
@flow
def build_and_run_pipeline():
    docker_task = build_and_run_docker()
    run_dbt(upstream_tasks=[docker_task])

# GitHub repository setup
source = GitRepository(
    url="https://github.com/Rickarddev-code/zoomcamp-project.git",  # Your GitHub repository URL
)

# Deploy the flow from GitHub repo
build_and_run_pipeline.from_source(
    source=source,
    entrypoint="prefect_pipeline.py:build_and_run_pipeline",  # The entry point is your prefect_pipeline.py file
).deploy(
    name="build-and-run-pipeline",  # Name of the deployment in Prefect Cloud
)
