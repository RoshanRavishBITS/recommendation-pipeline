import numpy as np
import pandas as pd
from .config import RAW, RANDOM_SEED

def generate_synthetic_data():
    rng = np.random.default_rng(RANDOM_SEED)
    n_users, n_items, n_events = 250, 100, 6000

    categories = ["Books", "Electronics", "Home", "Sports", "Beauty"]
    users = pd.DataFrame({
        "user_id": [f"U{i:04d}" for i in range(n_users)],
        "age": rng.integers(18, 66, n_users),
        "city": rng.choice(["Ranchi", "Delhi", "Mumbai", "Bengaluru", "Pune"], n_users),
        "signup_date": pd.Timestamp("2024-01-01") + pd.to_timedelta(rng.integers(0, 500, n_users), unit="D")
    })
    items = pd.DataFrame({
        "item_id": [f"I{i:04d}" for i in range(n_items)],
        "item_name": [f"Product {i:03d}" for i in range(n_items)],
        "category": rng.choice(categories, n_items),
        "price": np.round(rng.uniform(5, 500, n_items), 2)
    })

    # Give each user a soft category preference to create learnable patterns.
    user_pref = rng.integers(0, len(categories), n_users)
    events = []
    start = pd.Timestamp("2025-01-01")
    for e in range(n_events):
        u = int(rng.integers(0, n_users))
        preferred = categories[user_pref[u]]
        if rng.random() < 0.68:
            pool = items.index[items["category"] == preferred].to_numpy()
            it = int(rng.choice(pool))
        else:
            it = int(rng.integers(0, n_items))
        rating = int(np.clip(round(rng.normal(4.0 if items.loc[it, "category"] == preferred else 3.2, 0.9)), 1, 5))
        events.append((f"E{e:06d}", f"U{u:04d}", f"I{it:04d}", rating,
                       start + pd.to_timedelta(int(rng.integers(0, 600)), unit="D")))
    interactions = pd.DataFrame(events, columns=["interaction_id", "user_id", "item_id", "rating", "timestamp"])

    # Deliberately add a few data-quality defects for validation demonstration.
    bad = pd.DataFrame([
        ["BAD0001", "U0001", "I0001", 7, "2026-02-01"],
        ["BAD0002", "U0002", "I0002", 4, "not-a-date"],
        ["BAD0003", "U9999", "I0003", 5, "2026-02-02"],
        ["BAD0004", "U0004", "I9999", 3, "2026-02-03"],
        ["BAD0005", None, "I0005", 4, "2026-02-04"],
    ], columns=interactions.columns)
    interactions = pd.concat([interactions, bad, interactions.iloc[[0]]], ignore_index=True)

    users.to_csv(RAW / "users.csv", index=False)
    items.to_csv(RAW / "items.csv", index=False)
    interactions.to_csv(RAW / "interactions.csv", index=False)
    return users, items, interactions

def ingest_data():
    if not all((RAW / f).exists() for f in ("users.csv", "items.csv", "interactions.csv")):
        generate_synthetic_data()
    users = pd.read_csv(RAW / "users.csv")
    items = pd.read_csv(RAW / "items.csv")
    interactions = pd.read_csv(RAW / "interactions.csv")
    print(f"[INGESTION] users={len(users)}, items={len(items)}, interactions={len(interactions)}")
    return users, items, interactions
