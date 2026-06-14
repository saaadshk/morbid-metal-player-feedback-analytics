import requests
import pandas as pd
import time
from datetime import datetime

APP_ID = 1866130
BASE_URL = f"https://store.steampowered.com/appreviews/{APP_ID}"

all_reviews = []
seen_ids = set()

cursor = "*"
empty_pages = 0

while True:

    params = {
        "json": 1,
        "filter": "all",
        "language": "all",
        "review_type": "all",
        "purchase_type": "all",
        "num_per_page": 100,
        "cursor": cursor
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        print(f"Request failed: {response.status_code}")
        break

    data = response.json()

    reviews = data.get("reviews", [])

    if len(reviews) == 0:
        print("No reviews returned.")
        break

    new_reviews = 0

    for review in reviews:

        review_id = review.get("recommendationid")

        if review_id in seen_ids:
            continue

        seen_ids.add(review_id)
        new_reviews += 1

        all_reviews.append({
            "recommendation_id": review_id,
            "review_text": review.get("review", ""),
            "recommended": review.get("voted_up", False),
            "helpful_votes": review.get("votes_up", 0),
            "funny_votes": review.get("votes_funny", 0),
            "playtime_hours": round(
                review["author"].get("playtime_forever", 0) / 60,
                2
            ),
            "playtime_at_review_hours": round(
                review["author"].get("playtime_at_review", 0) / 60,
                2
            ),
            "review_date": datetime.fromtimestamp(
                review.get("timestamp_created", 0)
            ).strftime("%Y-%m-%d"),
            "early_access": review.get(
                "written_during_early_access",
                False
            )
        })

    print(
        f"Returned: {len(reviews)} | "
        f"Added: {new_reviews} | "
        f"Total Unique: {len(seen_ids)}"
    )

    # Steam sometimes repeats pages
    if new_reviews == 0:
        empty_pages += 1
    else:
        empty_pages = 0

    if empty_pages >= 5:
        print("Repeated pages detected. Stopping.")
        break

    cursor = data.get("cursor")

    if not cursor:
        print("No cursor returned.")
        break

    time.sleep(1)

df = pd.DataFrame(all_reviews)

df.drop_duplicates(
    subset=["recommendation_id"],
    inplace=True
)

df.to_csv(
    "morbid_metal_reviews.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nFinished!")
print(f"Total Unique Reviews: {len(df)}")