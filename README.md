# Tzadik Azaria — Portfolio V9.1 (refinement of V9)

Static site, no build step. Every link and asset path is relative, so it works from `/PortfolioV9/` on GitHub Pages (and from any folder or file://).

Upload the contents of this folder to the repo root (keep `.nojekyll`).

- `index.html` homepage · `campaign.html` `marketplace.html` `hatachana.html` `sambusak.html` · `about.html`
- `home.html` redirects to `index.html` (old links keep working)
- `styles.css` + `theme.css` (V8 foundation) · `v9.css` (V9 / V9.1 layer) · `app.js` · `fonts.css` (Archivo + Geist, embedded)
- `assets/` all project images, logo and CV
- `tools/build_v9.py` regenerates the HTML pages from one template (needs Pillow)

## Accent colour preview (the default site is unchanged: #E5091F)
- `accent-a.html` → Option A, current red #E5091F, with the accent used more sparingly
- `accent-b.html` → Option B, deeper red #BF3040, same reduced use, nothing else different
A small bar at the bottom-left switches between A / B and "Exit". The choice is remembered while you browse; "Exit" returns to the default site.
Remove the preview later by deleting the two `accent-*.html` files and the "accent preview" block at the top of `app.js` and the end of `v9.css`.


## V9.2 changes
- Hero rebuilt in a light, left-aligned style: large two-line headline, role label, curve with the weight/width twist, tagline + buttons row, hairline footer row. No red block, no floating elements.
- Black pill menu (white links, white "Download CV" button); mobile menu is a black overlay.
- Red is now a small accent (#BF3040): only the key curve point and the hero dot. The accent-preview pages were removed.
- The four case-study pages are long, image-led scrolls: big title + one line + metadata, full-width colour bands with minimal text, next-project band in the next project's colour. Same images, same labelling (Commercial work / Academic concept).
- Source of truth: tools/build_v9.py (run `python3 tools/build_v9.py`).

## V9.3 changes
- Type: Archivo + Geist replaced by Saira (variable, embedded). Display headings are bold, squared and uppercase; body text is Saira regular. The hero twist now animates Saira weight/width.
- Menu: smaller pill and logo (about 15px logo, 13.5px links).
- Hero: full-height, more space between label, headline, curve, tagline and the footer row.
- Case studies: larger paddings and gaps between bands, bigger spacing before the cover and next-project block, so the scroll is longer and airier.

## V9.4 changes
- Favicon: TZ monogram taken from the logo. favicon-tz-light.svg (black) for light browser themes, favicon-tz-dark.svg (white) for dark themes, apple-touch-icon-v94.png. New filenames avoid cached red icon; favicon.svg removed. Header logo and accent colour unchanged.
- Homepage grid: 12-column editorial composition. Campaign (wide) and Marketplace (tall, offset) lead; Hatachana (tall) and Give Me Sambusak (wide) mirror them. Larger, overlapping artwork inside the tiles. Titles, labels and links unchanged.
- Case studies: band padding and gallery gaps reduced; each project has its own composition (large + stacked supporting images, tall email beside banner and social, staggered phone screens, full-width icon strip, etc.). Images are never shown larger than their native width.
- Added previously unused work: Campaign (website mockup, social feed mockup), Marketplace (icon set, ingredient story, skincare benefits, razor refills).
- Source of truth: tools/build_v9.py.
