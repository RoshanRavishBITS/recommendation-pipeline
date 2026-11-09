from .pipeline import run_pipeline

try:
    from prefect import flow, task

    @task(name="execute-end-to-end-pipeline", retries=1, retry_delay_seconds=3)
    def pipeline_task():
        return run_pipeline()

    @flow(name="recommendation-data-management-pipeline", log_prints=True)
    def recommendation_pipeline():
        return pipeline_task()

except ImportError:
    def recommendation_pipeline():
        print("Prefect not installed; running sequential Python workflow.")
        return run_pipeline()

if __name__ == "__main__":
    recommendation_pipeline()
