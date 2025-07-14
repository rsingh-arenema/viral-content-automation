import os
import requests
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
PEXELS_API_URL = "https://api.pexels.com/videos/search"

def fetch_broll_videos(query, limit=3, out_dir="data/pexels"):
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query, "per_page": limit}

    response = requests.get(PEXELS_API_URL, headers=headers, params=params)
    if response.status_code != 200:
        print(f"[✖] Pexels API error: {response.status_code} {response.text}")
        return []

    os.makedirs(out_dir, exist_ok=True)

    downloaded = []
    for i, video in enumerate(response.json().get("videos", [])):
        video_url = video["video_files"][0]["link"]
        out_path = os.path.join(out_dir, f"clip_{i}.mp4")

        r = requests.get(video_url, stream=True)
        with open(out_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024):
                f.write(chunk)
        print(f"[✔] Downloaded: {out_path}")
        downloaded.append(out_path)

    return downloaded

# Test run
if __name__ == "__main__":
    fetch_broll_videos("space facts")
