# Final Project Report
## End-to-End Data Management Pipeline for a Recommendation System

### 1. Introduction and Objectives

The objective of this project is to develop a reproducible, end-to-end data management pipeline for an e-commerce recommendation system.

The pipeline manages the complete machine learning lifecycle, including data ingestion, validation, preparation, feature engineering, model training, evaluation, experiment tracking and workflow orchestration.

The implementation uses a modular Python architecture and supports two recommendation approaches: a popularity-based baseline and item-item collaborative filtering.

### 2. Architecture and Design Decisions

The pipeline follows seven major stages:

1. **Data ingestion:** Loads user, item and interaction datasets.
2. **Data validation:** Checks data quality, required fields, duplicates and invalid interactions. Rejected records are stored separately.
3. **Data preparation:** Cleans the interaction dataset and creates training and testing datasets.
4. **Feature management:** Generates user, item and interaction feature tables.
5. **Model training:** Trains a popularity baseline and an item-item collaborative filtering model.
6. **Model evaluation:** Compares models using Precision@5, Recall@5, NDCG@5, Coverage and Diversity.
7. **Orchestration and tracking:** Uses Prefect to coordinate execution and MLflow to record experiment metrics.

The modular design separates individual pipeline responsibilities, making the implementation easier to maintain, debug and extend.

### 3. Tools and Technologies

- **Python:** Main programming language.
- **Pandas and NumPy:** Data processing and preparation.
- **Scikit-learn / numerical modelling libraries:** Used where applicable for recommendation modelling and evaluation.
- **Prefect:** Pipeline orchestration and execution monitoring.
- **MLflow:** Experiment tracking and metric logging.
- **Git and GitHub:** Version control and project hosting.

### 4. Dataset and Data Preparation

The execution logs report:

- 250 users
- 100 items
- 6,006 input interactions
- 6,000 valid interactions
- 6 rejected interactions

The cleaned dataset was divided into:

- Training dataset: 4,802 interactions
- Testing dataset: 1,198 interactions

The counts reconcile: 6,006 input interactions minus 6 rejected interactions equals 6,000 valid interactions.

Feature engineering generated separate user, item and interaction feature tables.

### 5. Model Evaluation and Results

Two recommendation models were evaluated.

| Metric | Popularity Baseline | Item-Item Collaborative Filtering |
|---|---:|---:|
| Precision@5 | 0.0280 | 0.1496 |
| Recall@5 | 0.031848 | 0.175600 |
| NDCG@5 | 0.029212 | 0.170150 |
| Coverage | 0.14 | 0.86 |
| Diversity | 0.4344 | 0.2624 |

Item-item collaborative filtering achieved higher precision, recall, NDCG and coverage in this experiment. The popularity baseline achieved higher diversity.

These results indicate that collaborative filtering provided stronger recommendation relevance in the evaluated dataset, while the popularity baseline offered more diversity according to the implemented metric.

### 6. Orchestration and Experiment Tracking

The pipeline was executed successfully through Prefect. The execution logs show successful completion of ingestion, validation, preparation, feature generation, model training and evaluation.

MLflow was configured to track the recommendation-pipeline experiment. Model evaluation metrics were successfully logged, and the experiment is visible in the MLflow dashboard.

The source code, generated outputs, reports and execution screenshots are maintained in the GitHub repository.

### 7. Limitations and Future Improvements

The current implementation has several limitations:

- The dataset is relatively small, with 250 users and 100 items.
- Collaborative filtering performance depends on sufficient user-item interaction history.
- Offline evaluation does not guarantee equivalent performance in a live production environment.
- The project does not demonstrate online A/B testing or real-time recommendation serving.
- Further work could investigate hybrid recommendation models, cold-start handling, scalability and automated model monitoring.

### 8. Conclusion

The project successfully demonstrates an end-to-end data management and recommendation modelling workflow.

It integrates data ingestion, validation, preparation, feature management, model training, evaluation, orchestration and experiment tracking into a reproducible pipeline.

The experimental comparison shows that item-item collaborative filtering outperformed the popularity baseline on four of the five reported evaluation metrics.

The project provides a foundation for further development into a scalable recommendation system.
