# End-to-End Data Management Pipeline for a Recommendation System

A reproducible, CPU-friendly e-commerce recommendation pipeline built for the DM4ML Assignment 2.

## Pipeline

1. Data ingestion: users, items and user-item interactions (CSV).
2. Data validation: required fields, nulls, duplicates, types, rating range, timestamps and referential integrity. Rejected rows are written to `data/errors/`.
3. Preparation and transformation: cleaning, per-user time-based train/test split, user activity summaries, item popularity and user-item matrix.
4. Feature management: reusable user, item and interaction feature tables, plus `reports/feature_catalog.md`.
5. Model training: popularity baseline and personalized item-item collaborative filtering.
6. Evaluation: Precision@5, Recall@5, NDCG@5, catalog Coverage and category Diversity.
7. Orchestration: Prefect flow with task dependencies; MLflow experiment tracking when installed.

The project uses documented synthetic e-commerce data so it can run without paid APIs or a large download. The generator deliberately inserts a small number of invalid interaction rows to demonstrate validation and error handling.

## Requirements

- macOS, Windows or Linux
- Python 3.10–3.12 recommended
- Git (for GitHub submission)

## Setup (Mac)

Open Terminal and run:

```bash
cd ~/Desktop
unzip recommendation-pipeline.zip
cd recommendation-pipeline

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If `python3 --version` is below 3.10, install a current Python 3 release first.

## Run the complete pipeline

```bash
python -m src.orchestration
```

The first run creates deterministic synthetic raw CSVs, validates them, prepares datasets, builds features, trains both recommenders, evaluates them, and saves outputs. Run it again to reproduce the workflow.

You can also run without Prefect's orchestration UI by executing:

```bash
python -m src.pipeline
```

## Outputs to inspect

- `data/raw/`: generated users, items and interactions.
- `data/errors/invalid_interactions.csv`: rejected interaction records.
- `reports/validation_report.json`: validation counts and checks.
- `data/processed/`: clean interactions, train/test splits, activity summary, popularity and interaction matrix.
- `data/features/`: user, item and interaction feature tables.
- `models/`: serialized model artifacts.
- `reports/evaluation_results.csv`: side-by-side evaluation metrics.
- `reports/run_summary.json`: execution summary.
- `mlruns/`: local MLflow tracking data (if MLflow is installed).

## MLflow

MLflow is used for experiment tracking. After a successful run, launch its local UI in another Terminal tab:

```bash
mlflow ui --backend-store-uri ./mlruns
```

Open the local URL printed by MLflow (normally `http://127.0.0.1:5000`). The pipeline also writes a metrics CSV and JSON summary so the results remain available if the tracking UI is not running.

## Screenshots required for submission

Capture genuine screenshots from your own successful run. Do not use sample or fabricated screenshots.

1. Ingestion: Terminal showing generated/loaded users, items and interactions.
2. Validation: `reports/validation_report.json` and `data/errors/invalid_interactions.csv`.
3. Preparation: `data/processed/train_interactions.csv`, `test_interactions.csv`, and `user_item_matrix.csv`.
4. Features: `data/features/user_features.csv`, `item_features.csv`, `interaction_features.csv`.
5. Training: Terminal showing both models trained and files in `models/`.
6. Evaluation: `reports/evaluation_results.csv`.
7. Orchestration: Terminal showing Prefect flow completed successfully.
8. Experiment tracking: MLflow UI showing the experiment/runs (if available).

Save screenshots in `reports/screenshots/` with names `01_ingestion.png` through `08_mlflow.png`. Include the successful run output and GitHub repository URL in the final PDF.

## GitHub submission

Create an empty **public** GitHub repository named `recommendation-pipeline`. From the project folder:

```bash
git init
git add .
git commit -m "Build end-to-end recommendation data pipeline"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/recommendation-pipeline.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your actual GitHub username. Verify the repository opens in a private/incognito browser window before submitting. Do not put passwords, tokens or private data in the repository.

## Important academic note

This project is a working baseline implementation. Run it yourself, inspect the outputs, take your own execution screenshots, and make sure you can explain the design and limitations. Replace the GitHub placeholder in the final PDF with your real public repository URL.
