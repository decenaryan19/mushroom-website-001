from PIL import Image
from pathlib import Path

IMG = Path(__file__).resolve().parents[1] / "images"
specs = [
    ("hero-1.webp", "hero-1.png", 1280, 720, 65),
    ("hero-2.webp", "hero-2.png", 1280, 720, 65),
    ("hero-1-mobile.webp", "hero-1.png", 828, 466, 62),
    ("hero-2-mobile.webp", "hero-2.png", 828, 466, 62),
]
for dest, src, mw, mh, q in specs:
    img = Image.open(IMG / src).convert("RGB")
    img.thumbnail((mw, mh), Image.Resampling.LANCZOS)
    out = IMG / dest
    img.save(out, "WEBP", quality=q, method=6)
    print(f"{dest}: {out.stat().st_size // 1024} KB ({img.size[0]}x{img.size[1]})")
