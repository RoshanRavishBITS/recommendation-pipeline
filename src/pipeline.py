import json
from .config import REPORTS
from .ingestion import ingest_data
from .validation import validate_data
from .preparation import prepare_data
from .features import build_features
from .training import train_models
from .evaluation import evaluate_models
from .tracking import track_experiment

def run_pipeline():
    print("\n========== RECOMMENDATION PIPELINE START ==========")
    users, items, raw_interactions = ingest_data()
    clean = validate_data(users, items, raw_interactions)
    _, train, test, activity, popularity, matrix = prepare_data(users, items, clean)
    build_features(users, items, train, activity)
    model = train_models(train, items)
    results = evaluate_models(model, train, test, items)
    track_experiment(results)
    summary = {
        "status": "SUCCESS",
        "users": len(users), "items": len(items),
        "valid_interactions": len(clean), "train_interactions": len(train),
        "test_interactions": len(test),
        "models": ["Popularity baseline", "Item-item collaborative filtering"],
        "evaluation_file": "reports/evaluation_results.csv"
    }
    (REPORTS / "run_summary.json").write_text(json.dumps(summary, indent=2))
    print("========== RECOMMENDATION PIPELINE SUCCESS ==========\n")
    return summary

if __name__ == "__main__":
    run_pipeline()
