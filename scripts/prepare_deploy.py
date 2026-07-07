#!/usr/bin/env python3
"""Copy only production static assets to dist/ for Cloudflare Pages deploy."""
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
MAX_BYTES = 25 * 1024 * 1024  # Cloudflare Pages per-file limit

INCLUDE_FILES = ("index.html", "_headers")
INCLUDE_DIRS = ("css", "js", "pages", "fonts", "images")
ALLOWED_SUFFIXES = {".html", ".css", ".js", ".webp", ".woff2"}


def copy_tree(name: str) -> None:
    src_dir = ROOT / name
    if not src_dir.is_dir():
        return
    for path in src_dir.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in ALLOWED_SUFFIXES:
            continue
        rel = path.relative_to(src_dir)
        if rel.parts and rel.parts[0] == "raw":
            continue
        dest = DIST / name / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)


def main() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()

    for name in INCLUDE_FILES:
        src = ROOT / name
        if src.is_file():
            shutil.copy2(src, DIST / name)

    for name in INCLUDE_DIRS:
        copy_tree(name)

    large: list[tuple[int, Path]] = []
    total = 0
    count = 0
    for path in DIST.rglob("*"):
        if not path.is_file():
            continue
        size = path.stat().st_size
        total += size
        count += 1
        if size > MAX_BYTES:
            large.append((size, path.relative_to(DIST)))

    print(f"Prepared dist/: {count} files, {total / 1024:.0f} KB")
    if large:
        for size, rel in large:
            print(f"  OVER LIMIT: {rel} ({size / 1024 / 1024:.1f} MiB)")
        raise SystemExit("dist/ contains files over Cloudflare's 25 MiB limit")


if __name__ == "__main__":
    main()
