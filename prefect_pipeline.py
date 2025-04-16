from prefect import task, flow
from prefect_github import GitHubCredentials, GitHubRepository
import subprocess

# Define the task to run Docker container from Docker Hub
@task
def build_and_run_docker():
    print("Building and running the Docker container...")
    subprocess.run(["docker", "run", "-d", "--name", "zoomcamp-container", "rickardelliot/zoomcamp:latest"], check=True)
    print("Docker container started successfully.")

# Define the task to run DBT transformations
@task
def run_dbt():
    print("Running DBT transformations...")
    result = subprocess.run(["dbt", "run", "--project-dir", "zoomcamp_dbt"], capture_output=True, text=True)
    
    print(f"DBT run output: {result.stdout}")
    print(f"DBT run errors: {result.stderr}")
    
    if result.returncode != 0:
        raise Exception("DBT run failed")
    else:
        print("DBT transformations completed successfully.")

# Define the flow that will be scheduled and triggered from GitHub
@flow
def build_and_run_pipeline():
    print("Starting pipeline execution...")  # Check if this is printed
    docker_task = build_and_run_docker()
    print("Docker task finished. Now running DBT...")
    run_dbt(upstream_tasks=[docker_task])
    print("DBT task finished.")


# Load GitHub Blocks
print("Loading GitHub Blocks...")
github_repository_block = GitHubRepository.load("githubrespoitory")  # Replace with your actual block name
github_credentials_block = GitHubCredentials.load("githubtoken")  # Replace with your actual block name
print("GitHub Blocks loaded successfully.")
print(f"GitHub Repository Block: {github_repository_block}")
print(f"GitHub Credentials Block: {github_credentials_block}")

# Deploy the flow to Prefect Cloud
print("Deploying the flow...")
build_and_run_pipeline.from_source(
    source="https://github.com/Rickarddev-code/zoomcamp-project.git",  # GitHub repo URL
    entrypoint="prefect_pipeline.py:build_and_run_pipeline",  # Entry point of your flow
).deploy(
    name="build-and-run-pipeline-v2",
    work_pool_name="cloud_deploy",  # Specify the work pool name here
)
print("Flow deployed successfully.")
