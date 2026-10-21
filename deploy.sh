#!/bin/bash
# Publish the marketing page to the application VM (served by Caddy at
# verdictruntime.com/ (site root; /product/ 301s there) from /var/www/verdict-marketing), then check it's live.
set -euo pipefail
cd "$(dirname "$0")"
FILES=(index.html sample-report.html styles.css consent.js favicon.svg robots.txt sitemap.xml demo.mp4 demo-poster.jpg verdict-runtime-vs-snyk-codeql.pdf verdict-runtime-workflow.mp4 verdict-runtime-workflow-poster.jpg)
tar cz "${FILES[@]}" | gcloud compute ssh code-scanner --zone=us-central1-a \
  --command='sudo tar xz --no-same-owner -C /var/www/verdict-marketing'
live_title=$(curl -s https://verdictruntime.com/ | grep -o '<title>[^<]*</title>' || true)
local_title=$(grep -o '<title>[^<]*</title>' index.html)
if [ "$live_title" = "$local_title" ]; then
  echo "deployed: $live_title"
else
  echo "WARNING: live title '$live_title' != local '$local_title' (Cloudflare cache?)" >&2
  exit 1
fi
