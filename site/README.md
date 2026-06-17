# GameCodex Interactive Page

Static interactive page for the GameCodex project.

Open locally:

```text
G:\GameCodex\site\index.html
```

The page is intentionally static:

- no backend
- no live KataGo
- no raw CWI table in the browser
- precomputed data in `site/data/app-data.js`

Regenerate the page data:

```text
python scripts/export_site_data.py
```

For GitHub Pages, the simplest options are:

- serve the repository root and link to `/site/`
- or publish `site/` through a small Pages action later

The first public version should keep the claim narrow:

> AlphaGo did not create the largest structural shift in recorded Go. It accelerated how fast Go learns.
