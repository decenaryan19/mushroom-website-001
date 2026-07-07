#!/usr/bin/env python3
"""Fetch image URLs from suwanneebellfarms.com and download assets."""
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMG_DIR = ROOT / "images"
FONT_DIR = ROOT / "fonts"
IMG_DIR.mkdir(exist_ok=True)
FONT_DIR.mkdir(exist_ok=True)

BASE = "https://suwanneebellfarms.com"

def fetch(url, dest):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            dest.write_bytes(resp.read())
        print(f"OK  {dest.name}")
        return True
    except Exception as e:
        print(f"ERR {dest.name}: {e}")
        return False

html = urllib.request.urlopen(
    urllib.request.Request(BASE + "/", headers={"User-Agent": "Mozilla/5.0"}),
    timeout=60,
).read().decode("utf-8", "ignore")

urls = sorted(set(re.findall(r'https://suwanneebellfarms\.com/wp-content/uploads/[^"\')\s>]+\.(?:jpg|jpeg|png|webp)', html, re.I)))
print("Found URLs:")
for u in urls:
    print(" ", u)

# Map by filename hints
for url in urls:
    name = url.split("/")[-1].lower()
    if "logo" in name:
        fetch(url, IMG_DIR / "logo.webp")
    elif "hero" in name or "slider" in name or "banner" in name:
        pass

# Known mappings from page structure - fetch homepage and product page
pages = ["/", "/product/shiitake-mushrooms/", "/articles/"]
all_urls = set(urls)
for page in pages:
    try:
        phtml = urllib.request.urlopen(
            urllib.request.Request(BASE + page, headers={"User-Agent": "Mozilla/5.0"}),
            timeout=60,
        ).read().decode("utf-8", "ignore")
        all_urls.update(re.findall(r'https://suwanneebellfarms\.com/wp-content/uploads/[^"\')\s>]+\.(?:jpg|jpeg|png|webp)', phtml, re.I))
    except Exception as e:
        print(f"Page {page}: {e}")

print(f"\nTotal unique URLs: {len(all_urls)}")
for u in sorted(all_urls):
    print(u)

# Download all to images/raw then we'll rename
raw_dir = IMG_DIR / "raw"
raw_dir.mkdir(exist_ok=True)
for i, url in enumerate(sorted(all_urls)):
    fname = url.split("/")[-1]
    fetch(url, raw_dir / fname)

# Fonts
fonts = {
    "playfair-display-v37-latin-regular.woff2": "https://fonts.gstatic.com/s/playfairdisplay/v37/nuFiD-vYSZviVYUb_rj3ij__anPXDTzYgA.woff2",
    "playfair-display-v37-latin-600.woff2": "https://fonts.gstatic.com/s/playfairdisplay/v37/nuFiD-vYSZviVYUb_rj3ij__anPXDTLYgFE_.woff2",
    "playfair-display-v37-latin-700.woff2": "https://fonts.gstatic.com/s/playfairdisplay/v37/nuFiD-vYSZviVYUb_rj3ij__anPXDTPYgFE_.woff2",
}
for name, url in fonts.items():
    fetch(url, FONT_DIR / name)
