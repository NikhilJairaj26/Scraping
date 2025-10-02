import concurrent.futures
import requests
import pandas as pd
from tqdm import tqdm

# ---------- CONFIGURE ----------
API_KEY = "2392c894279bf23e20216d8f0205d625"  # Replace with your API key
CSV_FILE = "tmdb_movies_new.csv"
TOTAL_MOVIES = 15000
THREADS = 5
# -------------------------------

BASE_URL = "https://api.themoviedb.org/3/discover/movie"

# We’ll request movies sorted by popularity to get large variety
def fetch_page(page):
    params = {
        "api_key": API_KEY,
        "language": "en-US",
        "sort_by": "popularity.desc",
        "page": page,
        "include_adult": "false"
    }
    try:
        r = requests.get(BASE_URL, params=params, timeout=10)
        r.raise_for_status()
        return r.json().get("results", [])
    except Exception as e:
        print(f"❌ Error on page {page}: {e}")
        return []

def main():
    print(f"Fetching up to {TOTAL_MOVIES} movies from TMDb using {THREADS} threads...")

    total_pages = (TOTAL_MOVIES // 20) + 1
    all_movies = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = {executor.submit(fetch_page, page): page for page in range(1, total_pages + 1)}
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
            result = future.result()
            all_movies.extend(result)

    # Remove duplicates
    unique_movies = {m["id"]: m for m in all_movies}.values()

    # Prepare rich data
    data = []
    for m in unique_movies:
        data.append([
            m.get("id"),
            m.get("title"),
            m.get("release_date"),
            m.get("vote_average"),
            m.get("vote_count"),
            m.get("popularity"),
            m.get("overview"),
            m.get("original_language"),
            m.get("adult"),
            m.get("genre_ids"),
            m.get("original_title"),
            m.get("backdrop_path"),
            m.get("poster_path"),
            m.get("video"),
            m.get("original_language")
        ])

    df = pd.DataFrame(data, columns=[
        "ID", "Title", "Release_Date", "Rating", "Votes", "Popularity",
        "Overview", "Language", "Adult", "Genre_IDs", "Original_Title",
        "Backdrop_Path", "Poster_Path", "Video", "Original_Language"
    ])

    df.to_csv(CSV_FILE, index=False, encoding="utf-8")
    print(f"✅ Done! Saved {len(df)} unique movies to {CSV_FILE}")

if __name__ == "__main__":
    main()
