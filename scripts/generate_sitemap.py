#!/usr/bin/env python3
"""Generate sitemap.xml and robots.txt from HTML pages."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://suwanneebellfarms.com"

MAIN_PAGES = {"product", "articles", "about", "sample", "contact"}


def collect_pages() -> list[Path]:
    pages = [ROOT / "index.html"]
    pages_dir = ROOT / "pages"
    if pages_dir.is_dir():
        pages.extend(sorted(pages_dir.glob("*.html")))
    return pages


def page_url(rel_path: Path) -> str:
    if rel_path.name == "index.html" and rel_path.parent == Path("."):
        return f"{BASE_URL}/"
    return f"{BASE_URL}/{rel_path.as_posix()}"


def lastmod(path: Path) -> str:
    mtime = path.stat().st_mtime
    return datetime.fromtimestamp(mtime, tz=timezone.utc).strftime("%Y-%m-%d")


def priority(rel_path: Path) -> str:
    if rel_path.name == "index.html" and rel_path.parent == Path("."):
        return "1.0"
    if rel_path.stem in MAIN_PAGES:
        return "0.8"
    return "0.6"


def changefreq(rel_path: Path) -> str:
    if rel_path.name == "index.html" or rel_path.stem in MAIN_PAGES:
        return "weekly"
    return "monthly"


def generate_sitemap(dest: Path) -> int:
    entries: list[str] = []
    pages = collect_pages()
    for html_path in pages:
        rel = html_path.relative_to(ROOT)
        entries.append(
            f"""  <url>
    <loc>{page_url(rel)}</loc>
    <lastmod>{lastmod(html_path)}</lastmod>
    <changefreq>{changefreq(rel)}</changefreq>
    <priority>{priority(rel)}</priority>
  </url>"""
        )

    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(entries)
        + "\n</urlset>\n"
    )
    dest.write_text(xml, encoding="utf-8")
    return len(pages)


def generate_robots(dest: Path) -> None:
    dest.write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}/sitemap.xml\n",
        encoding="utf-8",
    )


def write_seo_files(out_dir: Path) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)
    count = generate_sitemap(out_dir / "sitemap.xml")
    generate_robots(out_dir / "robots.txt")
    return count


def main() -> None:
    count = write_seo_files(ROOT)
    print(f"Wrote sitemap.xml ({count} URLs) and robots.txt")


if __name__ == "__main__":
    main()
