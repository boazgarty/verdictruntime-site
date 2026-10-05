# verdictruntime-site

The public marketing page for Verdict Runtime. Plain HTML and CSS, no build
step, no JavaScript.

```
index.html     the page
styles.css     all styling, including both light and dark themes
favicon.svg    brand mark
_headers       response headers for Cloudflare Pages
netlify.toml   the same headers for Netlify
robots.txt     / sitemap.xml
```

## Deploying

**Live today (since 2026-10-05): served from the application VM**, by the same
Caddy that fronts the app. `verdictruntime.com/product/` serves the files in
`/var/www/verdict-marketing`; `www.verdictruntime.com/*` 308-redirects to
`verdictruntime.com/product/*`, so there is one canonical URL. Caddy config:
`/etc/caddy/Caddyfile` (recorded in `code-scanner-api/CLOUD.md`).

To publish a change, from this directory:

```bash
tar cz index.html sample-report.html styles.css consent.js favicon.svg robots.txt sitemap.xml \
  | gcloud compute ssh code-scanner --zone=us-central1-a \
      --command='sudo tar xz --no-same-owner -C /var/www/verdict-marketing'
```

The page is only up while the VM is: it is `STANDARD` (not Spot/preemptible,
checked 2026-10-05), but stopping it with `stop-gcp.sh` takes the marketing
page down with the app. `_headers`/`netlify.toml` are not read on the VM —
response headers come from Caddy.

**Alternative: a static host.** Cloudflare Pages (connect this repo, no build
command, output `/`, reads `_headers`) or Netlify (`netlify.toml` is ready)
would keep the page up independently of the VM. Moving there means removing
the `www` block from the Caddyfile and pointing `www` at the host instead.

## Before it goes live

- There is no `og:image`, so shared links render as a text-only preview. Adding
  a 1200x630 PNG and an `og:image` tag is the one real improvement left.
- The example finding in the hero is labelled as illustrative. Keep that label
  unless it is replaced with a real, published, permissioned example.

## Local preview

```bash
python3 -m http.server 8080
```

Then open <http://localhost:8080>. Response headers are applied by the host, so
they will not appear locally; verify them after deploying with
<https://securityheaders.com>.
