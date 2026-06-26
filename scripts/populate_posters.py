from __future__ import annotations

import csv
import os
from time import sleep

from config import DATASET_PATH, POSTER_MAP_PATH, TMDB_API_KEY

if __name__ == "__main__":
    if not TMDB_API_KEY:
        print("TMDB_API_KEY not set. Export TMDB_API_KEY and retry.")
        raise SystemExit(1)

    from services.preprocess import load_movies
    from services.tmdb_client import get_poster_url

    df = load_movies(DATASET_PATH)
    total = len(df)

    os.makedirs(os.path.dirname(POSTER_MAP_PATH), exist_ok=True)

    # Load existing progress
    processed = {}

    if os.path.exists(POSTER_MAP_PATH):
        with open(POSTER_MAP_PATH, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                processed[int(row["id"])] = row["poster_url"]

        print(f"Loaded {len(processed)} already processed movies.")

    file_exists = os.path.exists(POSTER_MAP_PATH)

    with open(POSTER_MAP_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["id", "poster_url"])

        print(f"Found {total} movies.")

        for idx, row in df.iterrows():

            movie_id = int(row["id"])

            if movie_id in processed:
                continue

            title = str(row["title"] or "")

            year = int(row["year"]) if row["year"] else None

            try:
                poster = get_poster_url(title, year)
            except Exception:
                poster = "/static/images/logo.png"

            writer.writerow([movie_id, poster])
            f.flush()

            processed[movie_id] = poster

            if len(processed) % 20 == 0:
                print(f"Processed {len(processed)}/{total}")

            sleep(0.2)

    print("Poster prefetch completed!")