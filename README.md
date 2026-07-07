# Suwannee Bell Farms — Mushroom Website

A high-performance static clone of [suwanneebellfarms.com](https://suwanneebellfarms.com/), built for **100 PageSpeed Insights** on mobile and desktop.

## Design tokens

| Token | Value |
|-------|-------|
| Cream background | `#fffdee` |
| Terracotta accent | `#de7e3d` |
| Forest green | `#3d7a3d` |
| Headings | Playfair Display (self-hosted WOFF2) |
| Body / UI | System UI stack (Type System) |

## Performance architecture

- **No CDN frameworks** — removed Tailwind CDN and Flickity
- **Self-hosted fonts** — Playfair Display only (~58 KB total); body uses `system-ui` (zero download)
- **Optimized WebP images** — responsive hero with mobile variants, lazy loading below the fold
- **Minimal JavaScript** — vanilla JS, deferred, no third-party scripts
- **No render-blocking Google Fonts or Maps iframe** — contact page uses a static map link
- **Cache headers** — `_headers` for long-lived static assets on Cloudflare Pages (1 year for CSS, JS, images, fonts)

## Project structure

```text
├── css/styles.css       # Single stylesheet
├── fonts/               # Self-hosted Playfair Display
├── images/              # Optimized WebP assets
├── js/script.js         # Hero, gallery, mobile menu
├── pages/               # Inner pages
├── scripts/             # Asset fetch & build helpers
├── _headers             # Cache policy
└── index.html           # Homepage
```

## Local development

```bash
python -m http.server 8765
```

Open `http://localhost:8765`

## Deploy

Deploy the folder root to **Cloudflare Pages** (or any static host). Run PageSpeed Insights against your live URL after deploy.

### Cloudflare Pages settings

For **Cloudflare Pages Git integration** (dashboard), use:

```text
Framework preset: None
Build command:    python scripts/prepare_deploy.py
Build output directory: dist
```

For **CLI deploy** from your machine:

```bash
npm run deploy
```

This builds a clean `dist/` folder (WebP, HTML, CSS, JS only — no `.git`, PNG originals, or dev files) then uploads it. Cloudflare rejects any single file over **25 MiB**; deploying the whole repo root (`.`) often fails because `.git` or large PNG sources get included.

Do not use `npx wrangler deploy` for this project. That command deploys a Worker and requires a `workers.dev` subdomain or route. This site is static and should deploy with `wrangler pages deploy dist`.

## Rebuild subpages

```bash
python scripts/build_pages.py
```

## Re-optimize images

```bash
python scripts/optimize_images.py
python scripts/optimize_hero.py
```

## Deploy for 100 mobile PageSpeed

**GitHub Pages** (`*.github.io`) serves static assets with a short ~10 minute cache TTL and cannot use `_headers`. Image delivery and non-blocking CSS matter most there.

**Cloudflare Pages** (recommended for cache audit) uses `_headers` automatically. Connect the repo in Cloudflare Pages, or add `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` secrets and push to `main` to use `.github/workflows/cloudflare-pages.yml`.

After any deploy, hard-refresh and re-run [PageSpeed Insights](https://pagespeed.web.dev/) on mobile.
