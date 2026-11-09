import pickle
import numpy as np
from .config import MODELS

def train_models(train, items):
    item_ids = sorted(items["item_id"].unique())
    item_to_idx = {v: i for i, v in enumerate(item_ids)}
    user_item = train.pivot_table(index="user_id", columns="item_id", values="rating", aggfunc="mean", fill_value=0)
    user_item = user_item.reindex(columns=item_ids, fill_value=0)
    X = user_item.to_numpy(dtype=float)

    # Popularity baseline scores items by interaction count.
    popularity = train.groupby("item_id").size().to_dict()

    # Item-item collaborative filtering: cosine similarity between item columns.
    item_vectors = X.T
    norms = np.linalg.norm(item_vectors, axis=1, keepdims=True)
    normalized = item_vectors / np.maximum(norms, 1e-12)
    similarity = normalized @ normalized.T
    np.fill_diagonal(similarity, 0.0)

    model = {
        "item_ids": item_ids,
        "item_to_idx": item_to_idx,
        "popularity": popularity,
        "similarity": similarity,
        "user_history": {
            u: dict(zip(g["item_id"], g["rating"]))
            for u, g in train.groupby("user_id")
        }
    }
    with open(MODELS / "popularity_model.pkl", "wb") as f:
        pickle.dump({"popularity": popularity, "item_ids": item_ids}, f)
    with open(MODELS / "item_item_cf_model.pkl", "wb") as f:
        pickle.dump(model, f)
    print("[TRAINING] popularity baseline and item-item collaborative filtering trained")
    return model
