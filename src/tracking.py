import json
from .config import REPORTS, ROOT

def track_experiment(results):
    try:
        import mlflow

        db_path = (ROOT / "mlflow.db").resolve()
        mlflow.set_tracking_uri(f"sqlite:///{db_path}")
        mlflow.set_experiment("recommendation-pipeline")

        with mlflow.start_run(run_name="synthetic-ecommerce-recommenders"):
            mlflow.log_param("dataset", "synthetic-ecommerce")
            mlflow.log_param("personalized_model", "item-item-collaborative-filtering")
            mlflow.log_param("k", 5)

            for _, row in results.iterrows():
                prefix = (
                    "popularity"
                    if row["Model"] == "Popularity baseline"
                    else "item_item_cf"
                )

                for metric in [
                    "Precision@5",
                    "Recall@5",
                    "NDCG@5",
                    "Coverage",
                    "Diversity"
                ]:
                    metric_name = metric.replace("@", "_at_")
                    mlflow.log_metric(
                        f"{prefix}_{metric_name}",
                        float(row[metric])
                    )

            mlflow.log_artifact(
                str(REPORTS / "evaluation_results.csv")
            )

        print("[TRACKING] Metrics successfully logged to MLflow")

    except Exception as exc:
        fallback = {
            "tracker": "JSON fallback",
            "reason": str(exc),
            "results": results.to_dict(orient="records")
        }

        (REPORTS / "tracking_fallback.json").write_text(
            json.dumps(fallback, indent=2)
        )

        print(f"[TRACKING] MLflow error: {exc}")

