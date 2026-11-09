import numpy as np
import pandas as pd
from .config import REPORTS, K

def recommend_popularity(model, seen, k=K):
    ranked = sorted(model["item_ids"], key=lambda x: model["popularity"].get(x, 0), reverse=True)
    return [x for x in ranked if x not in seen][:k]

def recommend_cf(model, user_id, k=K):
    seen_ratings = model["user_history"].get(user_id, {})
    scores = np.zeros(len(model["item_ids"]), dtype=float)
    for item, rating in seen_ratings.items():
        idx = model["item_to_idx"].get(item)
        if idx is not None:
            scores += model["similarity"][idx] * float(rating)
    seen = set(seen_ratings)
    ranked_idx = np.argsort(scores)[::-1]
    return [model["item_ids"][i] for i in ranked_idx if model["item_ids"][i] not in seen][:k]

def _metrics(recommendations, relevant_by_user, catalog, item_categories, k):
    precisions, recalls, ndcgs = [], [], []
    recommended_all = set()
    diversity_scores = []
    for user, relevant in relevant_by_user.items():
        recs = recommendations.get(user, [])[:k]
        hits = [1 if item in relevant else 0 for item in recs]
        precisions.append(sum(hits) / k)
        recalls.append(sum(hits) / max(1, len(relevant)))
        dcg = sum(hit / np.log2(i + 2) for i, hit in enumerate(hits))
        ideal = sum(1 / np.log2(i + 2) for i in range(min(len(relevant), k)))
        ndcgs.append(dcg / ideal if ideal else 0.0)
        recommended_all.update(recs)
        cats = {item_categories.get(x, "Unknown") for x in recs}
        diversity_scores.append(len(cats) / max(1, len(recs)))
    return {
        "Precision@5": float(np.mean(precisions)) if precisions else 0.0,
        "Recall@5": float(np.mean(recalls)) if recalls else 0.0,
        "NDCG@5": float(np.mean(ndcgs)) if ndcgs else 0.0,
        "Coverage": float(len(recommended_all) / max(1, len(catalog))),
        "Diversity": float(np.mean(diversity_scores)) if diversity_scores else 0.0
    }

def evaluate_models(model, train, test, items):
    relevant = test.groupby("user_id")["item_id"].apply(set).to_dict()
    categories = items.set_index("item_id")["category"].to_dict()
    catalog = set(items["item_id"])
    users = sorted(relevant)
    pop_recs, cf_recs = {}, {}
    for u in users:
        seen = set(train.loc[train["user_id"] == u, "item_id"])
        pop_recs[u] = recommend_popularity(model, seen)
        cf_recs[u] = recommend_cf(model, u)
    rows = []
    for name, recs in (("Popularity baseline", pop_recs), ("Item-item collaborative filtering", cf_recs)):
        row = {"Model": name}
        row.update(_metrics(recs, relevant, catalog, categories, K))
        rows.append(row)
    result = pd.DataFrame(rows)
    result.to_csv(REPORTS / "evaluation_results.csv", index=False)
    print("[EVALUATION] results saved to reports/evaluation_results.csv")
    print(result.to_string(index=False))
    return result
