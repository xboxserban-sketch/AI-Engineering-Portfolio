"""
Video B-Roll Hunter: Sourcing authentic, free HD cinematic video b-roll (fog, rain, night roads, police lights)
from open repositories and generative motion loops. Elevates the documentary from a static slideshow
to a living, breathing cinematic motion picture (stil Lemmino / MagnatesMedia).
"""

import os
import requests
from typing import List, Optional


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def search_wikimedia_videos(query: str, limit: int = 3) -> List[str]:
    """Searches Wikimedia Commons for authentic public domain video files (.webm, .mp4, .ogv)."""
    url = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": f"{query} filetype:video",
        "gsrnamespace": 6,
        "gsrlimit": limit,
        "prop": "imageinfo",
        "iiprop": "url|mime",
        "format": "json"
    }
    videos = []
    try:
        res = requests.get(url, params=params, headers=HEADERS, timeout=8).json()
        pages = res.get("query", {}).get("pages", {})
        for _, page in pages.items():
            info = page.get("imageinfo", [{}])[0]
            vurl = info.get("url")
            if vurl and any(vurl.lower().endswith(ext) for ext in [".webm", ".mp4", ".ogv"]):
                videos.append(vurl)
    except Exception as e:
        print(f"  [Video Hunter Error] {e}")
    return videos


def download_broll_video(video_url: str, output_path: str) -> Optional[str]:
    """Downloads an authentic HD video clip."""
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    try:
        resp = requests.get(video_url, headers=HEADERS, stream=True, timeout=20)
        if resp.status_code == 200:
            with open(output_path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)
            print(f"  [Video Hunter] Acquired HD B-Roll Video: {output_path}")
            return output_path
    except Exception as e:
        print(f"  [Video Hunter Error] Download failed: {e}")
    return None


if __name__ == "__main__":
    print("Video B-Roll Hunter loaded.")
