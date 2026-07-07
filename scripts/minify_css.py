#!/usr/bin/env python3
"""Minify css/styles.css to css/styles.min.css."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "css" / "styles.css"
DEST = ROOT / "css" / "styles.min.css"

def minify_css(css: str) -> str:
    # Remove comments
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)
    # Remove whitespace around operators and brackets
    css = re.sub(r'\s*([\{\};:,])\s*', r'\1', css)
    # Remove duplicate whitespace
    css = re.sub(r'\s+', ' ', css)
    # Remove trailing semicolon before closing bracket
    css = re.sub(r';\}', '}', css)
    return css.strip()

def main() -> None:
    if not SRC.exists():
        print(f"Error: {SRC} does not exist.")
        return
    css = SRC.read_text(encoding="utf-8")
    minified = minify_css(css)
    DEST.write_text(minified, encoding="utf-8")
    print(f"Minified {SRC.stat().st_size / 1024:.1f} KB -> {DEST.stat().st_size / 1024:.1f} KB")

if __name__ == "__main__":
    main()
