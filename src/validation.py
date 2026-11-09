import pandas as pd
from .config import ERRORS, REPORTS

def validate_data(users, items, interactions):
    required = ["interaction_id", "user_id", "item_id", "rating", "timestamp"]
    df = interactions.copy()
    issues = pd.DataFrame(index=df.index)
    issues["missing_required"] = df[required].isna().any(axis=1)
    issues["duplicate_interaction_id"] = df["interaction_id"].duplicated(keep="first")
    rating = pd.to_numeric(df["rating"], errors="coerce")
    issues["invalid_rating_or_type"] = rating.isna() | ~rating.between(1, 5)
    ts = pd.to_datetime(df["timestamp"], errors="coerce")
    issues["invalid_timestamp"] = ts.isna()
    issues["unknown_user"] = ~df["user_id"].isin(users["user_id"])
    issues["unknown_item"] = ~df["item_id"].isin(items["item_id"])
    invalid_mask = issues.any(axis=1)
    rejected = df.loc[invalid_mask].copy()
    rejected["validation_errors"] = issues.loc[invalid_mask].apply(
        lambda row: ";".join(row.index[row.values]), axis=1
    )
    clean = df.loc[~invalid_mask].copy()
    clean["rating"] = rating.loc[~invalid_mask].astype(float)
    clean["timestamp"] = ts.loc[~invalid_mask]
    rejected.to_csv(ERRORS / "invalid_interactions.csv", index=False)

    report = {
        "input_interactions": int(len(df)),
        "valid_interactions": int(len(clean)),
        "rejected_interactions": int(len(rejected)),
        "checks": {
            "missing_required_fields": int(issues["missing_required"].sum()),
            "duplicate_interaction_ids": int(issues["duplicate_interaction_id"].sum()),
            "invalid_rating_or_type": int(issues["invalid_rating_or_type"].sum()),
            "invalid_timestamps": int(issues["invalid_timestamp"].sum()),
            "unknown_users": int(issues["unknown_user"].sum()),
            "unknown_items": int(issues["unknown_item"].sum())
        },
        "status": "PASS" if len(clean) > 0 else "FAIL"
    }
    import json
    (REPORTS / "validation_report.json").write_text(json.dumps(report, indent=2))
    print(f"[VALIDATION] valid={len(clean)}, rejected={len(rejected)}; report saved")
    return clean
