from prefect import task, flow
from prefect_github import GitHubCredentials, GitHubRepository  # Add this import
import subprocess

# Define the task to run Docker container from Docker Hub
@task
def build_and_run_docker():
    print("Building and running the Docker container...")
    subprocess.run(["docker", "run", "-d", "--name", "zoomcamp-container", "rickardelliot/zoomcamp:latest"], check=True)
    print("Docker container started successfully.")

@task
def run_dbt():
    print("Running DBT transformations...")
    subprocess.run(["dbt", "run", "--project-dir", "zoomcamp_dbt"], check=True)
    print("DBT transformations completed.")


# Define the flow that will be scheduled and triggered from GitHub
@flow
def build_and_run_pipeline():
    docker_task = run_docker_from_hub()
    run_dbt(upstream_tasks=[docker_task])

print("Loading GitHub Blocks...")
github_repository_block = GitHubRepository.load("githubrespoitory")  # Replace with your actual block name
github_credentials_block = GitHubCredentials.load("githubtoken")  # Replace with your actual block name
print("Blocks loaded successfully.")

print("Deploying the flow...")
build_and_run_pipeline.from_source(
    source="https://github.com/Rickarddev-code/zoomcamp-project.git",
    entrypoint="prefect_pipeline.py:build_and_run_pipeline",
).deploy(
    name="build-and-run-pipeline-v2",
    work_pool_name="cloud_deploy",
)
print("Flow deployed.")
