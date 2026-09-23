"""
Asset Hunter: Multi-tier authentic archival image acquisition engine.
Sources:
1. Wikimedia Commons API (Direct historical public-domain archives, charts, mugshots)
2. Wikipedia Media API (Article leads and verified historical photography)
3. DuckDuckGo Image Search (General web images with rate-limit protection)
4. Case File Dossier Generator (High-end noir archival fallback)
All outputs are color-graded to Nordic Noir / 35mm Vintage 1920x1080.
"""

import io
import os
import random
import time
import requests
from typing import List, Optional
from PIL import Image, ImageOps, ImageEnhance, ImageFilter, ImageDraw, ImageFont


HEADERS = {
    "User-Agent": "CinematicDocBot/2.0 (Historical Documentary Educational Research; mailto:contact@docengine.local)"
}


def search_wikimedia_commons(query: str, limit: int = 5) -> List[str]:
    """Searches Wikimedia Commons specifically for historical & archival image files."""
    url = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": query,
        "gsrnamespace": 6,  # File namespace
        "gsrlimit": limit,
        "prop": "imageinfo",
        "iiprop": "url",
        "format": "json"
    }
    candidates = []
    try:
        res = requests.get(url, params=params, headers=HEADERS, timeout=8).json()
        pages = res.get("query", {}).get("pages", {})
        for _, page in pages.items():
            info = page.get("imageinfo", [{}])[0]
            img_url = info.get("url")
            if img_url:
                base_url = img_url.split("?")[0].lower()
                if any(base_url.endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".webp"]):
                    candidates.append(img_url)
    except Exception as e:
        print(f"    [Wikimedia Error] {e}")
    return candidates


def search_ddg_images(query: str, limit: int = 5) -> List[str]:
    """Searches DuckDuckGo with safety checks and clean exception handling."""
    candidates = []
    try:
        try:
            from ddgs import DDGS
        except ImportError:
            from duckduckgo_search import DDGS
            
        with DDGS() as ddgs:
            results = list(ddgs.images(query, max_results=limit))
            for r in results:
                url = r.get("image")
                if url and url.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                    candidates.append(url)
    except Exception:
        pass
    return candidates


def search_and_download_image(query: str, output_path: str, max_candidates: int = 6) -> str:
    """
    Tiered search strategy:
    Tier 1: Wikimedia Commons archival files.
    Tier 2: DuckDuckGo image search.
    Tier 3: Procedural Case File Dossier Generator.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    print(f"  [Hunter] Sourcing visuals for: '{query}'...")

    candidates = []
    
    # 1. Try Wikimedia Commons with query and relaxed variants
    words = [w for w in query.split() if w.lower() not in ["archive", "black", "white", "history", "documentary", "dark", "room"]]
    clean_query = " ".join(words[:3])
    commons_results = search_wikimedia_commons(clean_query, limit=4)
    if not commons_results and len(words) >= 2:
        commons_results = search_wikimedia_commons(" ".join(words[:2]), limit=4)
    candidates.extend(commons_results)
    
    # 2. Try DuckDuckGo if needed
    if len(candidates) < 2:
        time.sleep(0.2)
        ddg_results = search_ddg_images(f"{clean_query} vintage photo", limit=3)
        candidates.extend(ddg_results)
        
    downloaded = False
    for url in candidates[:max_candidates]:
        try:
            resp = requests.get(url, headers=HEADERS, timeout=8)
            if resp.status_code == 200 and len(resp.content) > 12000:
                raw_img = Image.open(io.BytesIO(resp.content)).convert("RGB")
                processed_img = process_cinematic_frame(raw_img)
                processed_img.save(output_path, "JPEG", quality=95)
                downloaded = True
                print(f"  [Hunter] Acquired authentic archive visual: {output_path}")
                break
        except Exception:
            continue

    if not downloaded:
        print(f"  [Hunter] Rendering procedural dark noir dossier frame for: '{query}'...")
        dossier = generate_dossier_frame(query)
        dossier.save(output_path, "JPEG", quality=95)

    return output_path


def process_cinematic_frame(img: Image.Image, target_width: int = 1920, target_height: int = 1080) -> Image.Image:
    """
    Fits and crops to 16:9, sharpens, and applies Nordic Noir / Archive grading.
    """
    fitted = ImageOps.fit(img, (target_width, target_height), method=Image.Resampling.LANCZOS, centering=(0.5, 0.45))
    
    # Desaturate slightly for authentic documentary realism
    desaturated = ImageEnhance.Color(fitted).enhance(0.55)
    
    # Boost contrast
    high_contrast = ImageEnhance.Contrast(desaturated).enhance(1.28)
    
    # Sharpen
    sharpened = high_contrast.filter(ImageFilter.UnsharpMask(radius=1.5, percent=120, threshold=3))
    
    # Color grading: Cold mystery shadows, warm highlights
    r, g, b = sharpened.split()
    r = r.point(lambda i: int(i * 0.94))
    b = b.point(lambda i: min(255, int(i * 1.06)))
    return Image.merge("RGB", (r, g, b))


def generate_dossier_frame(topic: str, target_width: int = 1920, target_height: int = 1080) -> Image.Image:
    """
    Renders an authentic, stylish FBI/Investigation dossier frame
    with stamp, grid coordinates, and typewriter typography.
    """
    img = Image.new("RGB", (target_width, target_height), (12, 16, 22))
    draw = ImageDraw.Draw(img)
    
    # Grid lines
    for x in range(0, target_width, 160):
        draw.line([(x, 0), (x, target_height)], fill=(20, 26, 35), width=1)
    for y in range(0, target_height, 120):
        draw.line([(0, y), (target_width, y)], fill=(20, 26, 35), width=1)
        
    # Vignette shadow
    draw.rectangle([60, 60, target_width - 60, target_height - 60], outline=(35, 45, 60), width=2)
    
    # Dossier stamps
    draw.rectangle([100, 100, 360, 150], fill=(130, 24, 24))
    
    font = ImageFont.load_default()
    draw.text((120, 118), "EVIDENCE DOSSIER // CLASSIFIED", font=font, fill=(255, 255, 255))
    draw.text((100, 200), f"SUBJECT: {topic.upper()[:60]}", font=font, fill=(180, 200, 220))
    draw.text((100, 240), f"STATUS: UNSOLVED // ACTIVE COGNITIVE INVESTIGATION", font=font, fill=(140, 160, 180))
    draw.text((100, 280), f"CASE ARCHIVE FILE REF: #DOC-{random.randint(1000, 9999)}-X", font=font, fill=(110, 130, 150))
    
    return img


if __name__ == "__main__":
    test_out = "output/test_wikimedia_archive.jpg"
    search_and_download_image("Flannan Isles lighthouse", test_out)
