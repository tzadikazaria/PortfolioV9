# Tzadik Azaria — Portfolio V9

Static site built on V8. Open `index.html` (no build step needed).

- `index.html` homepage · `campaign.html`, `marketplace.html`, `hatachana.html`, `sambusak.html` case studies · `about.html`
- `home.html` is a redirect to `index.html` (old links keep working)
- `styles.css` + `theme.css` = V8 foundation (unchanged) · `v9.css` = V9 layer · `app.js` = all behaviour
- `assets/` = all original V8 images, fonts and CV (nothing removed)
- `_archive/` = V8 originals that are no longer part of the site (old pages, concept prototypes, legacy /work pages)
- `tools/build_v9.py` (needs Pillow) regenerates the pages from one template
