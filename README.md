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

Either host works and both are free at this volume. Pick one — deploying to
both means two copies of the same page competing in search results.

**Cloudflare Pages** — create a project, connect this repository, and set the
build command to none and the output directory to `/`. Reads `_headers`.

**Netlify** — "Add new site" → import this repository. `netlify.toml` already
declares no build command and publishes the repository root.

Then add the custom domain in the host's dashboard and create **one CNAME
record** at your DNS provider:

```
www   CNAME   <the hostname your host gives you>
```

A subdomain is a plain CNAME and works on any DNS provider. The bare apex
(`verdictruntime.com` with no prefix) cannot take a CNAME, so pointing the apex
here means either moving nameservers to Cloudflare or using your host's apex
support. Starting on `www` avoids that entirely.

Keep the product UI on its own subdomain (`app.verdictruntime.com`). Do not
serve this page from the application VM: that instance is preemptible, and a
marketing page that is down when a prospect clicks is worse than no page.

## Before it goes live

- `security@verdictruntime.com` in `index.html` is a placeholder. Create the
  mailbox or change the address.
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
