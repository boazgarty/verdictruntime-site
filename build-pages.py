#!/usr/bin/env python3
"""Generate the topic pages (/benchmark/, /how-it-works/, ...) from index.html.

index.html stays the single source of truth: each page copies its section(s)
verbatim from it, adds its own title/description/canonical, and reuses the
home page's nav, closing CTA, footer and cookie banner. Re-run after editing
index.html (deploy.sh does it automatically).
"""
import html
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent
SITE = "https://verdictruntime.com"

# slug, section ids/headings to copy, <title>, meta description, eyebrow, h1
PAGES = [
    ("benchmark", ["id=\"benchmark\""],
     "Benchmark vs Snyk and CodeQL - Verdict Runtime",
     "How Verdict Runtime compares with Snyk and CodeQL on real, labelled vulnerable applications: dependency findings, code findings and severity agreement.",
     "Benchmark", "Verdict Runtime vs Snyk and CodeQL"),
    ("how-it-works", ["id=\"how\"", "Every finding says how sure we are"],
     "How It Works - Verdict Runtime",
     "Find it, prove it, fix it, protect it: how Verdict Runtime scans, verifies exploits live against your running app, prepares fixes and labels every finding with its evidence.",
     "How it works", "How Verdict Runtime works"),
    ("coverage", ["id=\"coverage\""],
     "Coverage - OWASP Web, API and LLM Top 10 - Verdict Runtime",
     "What Verdict Runtime covers: code, dependencies, IaC, secrets, containers, cloud and Kubernetes posture, and live testing across the OWASP Web, API and LLM Top 10.",
     "Coverage", "What Verdict Runtime covers"),
    ("defense", ["id=\"defense\""],
     "Defense and Virtual Patching - Verdict Runtime",
     "Stay protected while the fix is in review: WAF virtual patches, API gateway rules, detection rules and guardrails generated from verified findings.",
     "Defense", "Defense and virtual patching"),
    ("integrations", ["id=\"integrations\""],
     "Integrations - Verdict Runtime",
     "Verdict Runtime from the IDE to production: pull request checks, CI, ticketing, SIEM and WAF integrations.",
     "Integrations", "Verdict Runtime integrations"),
    ("deployment", ["id=\"deploy\""],
     "Deployment and Self-Hosting - Verdict Runtime",
     "Run Verdict Runtime as a hosted service or self-host it in your own network so your code never leaves it.",
     "Deployment", "Deployment and self-hosting"),
    ("security", ["Nothing runs without your written scope", "Held to the standard it sells"],
     "Security and Authorisation - Verdict Runtime",
     "How Verdict Runtime keeps testing safe: nothing runs without your written scope, and the method is held to the standard it sells.",
     "Security", "Security and authorisation"),
    ("faq", ["id=\"faq\""],
     "FAQ - Verdict Runtime",
     "Answers to the questions security teams ask first about Verdict Runtime: data handling, production testing, false positives, pricing and more.",
     "FAQ", "Frequently asked questions"),
]

NAV_TO_PAGE = {"#benchmark": "benchmark", "#how": "how-it-works", "#coverage": "coverage",
               "#defense": "defense", "#integrations": "integrations",
               "#deploy": "deployment", "#faq": "faq"}


def sections(src: str) -> list[str]:
    return re.findall(r"  <section\b.*?</section>\n", src, re.S)


def pick(all_secs: list[str], key: str) -> str:
    hits = [s for s in all_secs if key in s]
    if len(hits) != 1:
        raise SystemExit(f"build-pages: expected exactly one section matching {key!r}, found {len(hits)}")
    return hits[0]


def absolutize(fragment: str) -> str:
    """Pages live one directory down, so relative asset links become root-relative."""
    def fix(m):
        attr, val = m.group(1), m.group(2)
        if re.match(r"(https?:|mailto:|/|data:)", val):
            return m.group(0)
        return f'{attr}="/{val}"'
    return re.sub(r'\b(href|src|poster)="([^"]*)"', fix, fragment)


def between(src: str, start: str, end: str) -> str:
    i = src.index(start)
    return src[i:src.index(end, i) + len(end)]


def main() -> None:
    src = (ROOT / "index.html").read_text()
    head_tail = between(src, '<link rel="preconnect"', "</head>")
    nav = between(src, '<nav class="topnav"', "</nav>")
    for anchor, slug in NAV_TO_PAGE.items():
        nav = nav.replace(f'href="{anchor}"', f'href="/{slug}/"')
    nav = nav.replace('href="#top"', 'href="/"')
    cta = between(src, '  <div class="cta">', "\n  </div>\n")
    footer = between(src, "  <footer>", "</footer>")
    banner = between(src, '<div id="consent-banner"', "</div>\n</div>")
    all_secs = sections(src)

    for slug, keys, title, desc, eyebrow, h1 in PAGES:
        url = f"{SITE}/{slug}/"
        t, d = html.escape(title), html.escape(desc)
        body = "\n".join(pick(all_secs, k) for k in keys)
        page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
<link rel="canonical" href="{url}">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Verdict Runtime">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary_large_image">
{head_tail}
<body>

{nav}

<div class="wrap" id="top">

  <div class="hero hero-page">
    <h1>{html.escape(h1)}</h1>
    <p class="lede">{d}</p>
  </div>

{body}
{cta}

{footer}

</div>

{banner}

</body>
</html>
"""
        out = ROOT / slug / "index.html"
        out.parent.mkdir(exist_ok=True)
        out.write_text(absolutize(page))
    print(f"build-pages: wrote {len(PAGES)} pages")


if __name__ == "__main__":
    main()
