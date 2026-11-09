import pandas as pd
from .config import PROCESSED, TEST_FRACTION

def prepare_data(users, items, interactions):
    clean = interactions.drop_duplicates(subset=["interaction_id"]).copy()
    clean = clean.sort_values(["user_id", "timestamp"])
    # Per-user chronological holdout: latest 20% of each user's interactions.
    train_parts, test_parts = [], []
    for _, group in clean.groupby("user_id"):
        group = group.sort_values("timestamp")
        if len(group) >= 3:
            n_test = max(1, int(round(len(group) * TEST_FRACTION)))
            train_parts.append(group.iloc[:-n_test])
            test_parts.append(group.iloc[-n_test:])
        else:
            train_parts.append(group)
    train = pd.concat(train_parts, ignore_index=True) if train_parts else clean.iloc[0:0]
    test = pd.concat(test_parts, ignore_index=True) if test_parts else clean.iloc[0:0]
    clean.to_csv(PROCESSED / "clean_interactions.csv", index=False)
    train.to_csv(PROCESSED / "train_interactions.csv", index=False)
    test.to_csv(PROCESSED / "test_interactions.csv", index=False)

    activity = train.groupby("user_id").agg(
        user_activity_count=("interaction_id", "count"),
        user_average_rating=("rating", "mean"),
        last_interaction=("timestamp", "max")
    ).reset_index()
    activity.to_csv(PROCESSED / "user_activity_summary.csv", index=False)

    popularity = train.groupby("item_id").agg(
        item_popularity=("interaction_id", "count"),
        item_average_rating=("rating", "mean")
    ).reset_index().sort_values(["item_popularity", "item_average_rating"], ascending=False)
    popularity.to_csv(PROCESSED / "item_popularity.csv", index=False)

    matrix = train.pivot_table(index="user_id", columns="item_id", values="rating", aggfunc="mean", fill_value=0)
    matrix.to_csv(PROCESSED / "user_item_matrix.csv")
    print(f"[PREPARATION] clean={len(clean)}, train={len(train)}, test={len(test)}")
    return clean, train, test, activity, popularity, matrix
