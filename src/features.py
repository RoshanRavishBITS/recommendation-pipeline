import pandas as pd
from .config import FEATURES

def build_features(users, items, train, activity):
    user_features = users.merge(activity, on="user_id", how="left")
    user_features["user_activity_count"] = user_features["user_activity_count"].fillna(0).astype(int)
    user_features["user_average_rating"] = user_features["user_average_rating"].fillna(0)
    user_features["preferred_category"] = (
        train.merge(items[["item_id", "category"]], on="item_id")
             .groupby(["user_id", "category"]).size().reset_index(name="n")
             .sort_values(["user_id", "n"], ascending=[True, False])
             .drop_duplicates("user_id").set_index("user_id")["category"]
    )
    user_features["preferred_category"] = user_features["user_id"].map(user_features["user_id"].map(
        user_features.set_index("user_id")["preferred_category"]
    )) if False else user_features["user_id"].map(
        train.merge(items[["item_id", "category"]], on="item_id")
             .groupby(["user_id", "category"]).size().reset_index(name="n")
             .sort_values(["user_id", "n"], ascending=[True, False])
             .drop_duplicates("user_id").set_index("user_id")["category"]
    )
    user_features["preferred_category"] = user_features["preferred_category"].fillna("Unknown")
    user_features.to_csv(FEATURES / "user_features.csv", index=False)

    item_stats = train.groupby("item_id").agg(
        item_popularity=("interaction_id", "count"),
        item_average_rating=("rating", "mean"),
        last_interaction=("timestamp", "max")
    ).reset_index()
    item_features = items.merge(item_stats, on="item_id", how="left")
    item_features["item_popularity"] = item_features["item_popularity"].fillna(0).astype(int)
    item_features["item_average_rating"] = item_features["item_average_rating"].fillna(0)
    item_features.to_csv(FEATURES / "item_features.csv", index=False)

    last_by_user = train.groupby("user_id")["timestamp"].max()
    interaction_features = train.copy()
    interaction_features["user_last_interaction"] = interaction_features["user_id"].map(last_by_user)
    interaction_features["days_since_user_last_interaction"] = (
        interaction_features["user_last_interaction"] - interaction_features["timestamp"]
    ).dt.days
    interaction_features.to_csv(FEATURES / "interaction_features.csv", index=False)
    print("[FEATURES] user, item and interaction feature tables saved")
    return user_features, item_features, interaction_features
