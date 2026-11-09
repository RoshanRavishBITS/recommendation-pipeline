# Feature Catalog

| Feature | Entity | Definition | Source / computation | Reuse |
|---|---|---|---|---|
| age | User | User age in years | `users.csv` | Training and serving |
| city | User | User city | `users.csv` | Training and serving |
| user_activity_count | User | Number of training interactions | Count interactions by user | Training and serving |
| user_average_rating | User | Mean rating given by user | Mean training rating by user | Training and serving |
| preferred_category | User | Most-interacted-with category | Mode of user's training item categories | Training and serving |
| item_popularity | Item | Number of training interactions | Count interactions by item | Ranking and serving |
| item_average_rating | Item | Mean training rating | Mean rating by item | Ranking and serving |
| category | Item | Product category | `items.csv` | Content features and diversity |
| price | Item | Product price | `items.csv` | Content features and ranking |
| days_since_user_last_interaction | Interaction | Age in days relative to user's latest training interaction | Latest user timestamp minus event timestamp | Recency features |

All aggregate features are computed from the training partition to avoid using held-out test interactions.
