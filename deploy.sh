#!/bin/bash
# Deploy the /diet/ page on mihaicosma.com.
#
# Source:  /code/website/diet/index.html  (the static page)
# Target:  mc-new:/var/www/mihaicosma.com/diet/index.html  (live)
#
# Only the /diet/ subfolder of the live site is touched — the rest of
# mihaicosma.com is left alone. data.json is served from the jsDelivr CDN
# (cdn.jsdelivr.net/gh/wakamex/diet@main/site/data.json) and refreshes on
# every push to the diet repo, so this script handles only the page itself.

set -euo pipefail

SRC="/code/website/diet/index.html"
ZONE="us-central1-a"
HOST="mc-new"
TARGET_DIR="/var/www/mihaicosma.com/diet"

if [ ! -f "$SRC" ]; then
    echo "ERROR: $SRC not found — nothing to deploy" >&2
    exit 1
fi

STAGED="$(mktemp -u diet-index.XXXXXX.html)"

echo "→ scp  $SRC → $HOST:~/$STAGED"
gcloud compute scp "$SRC" "$HOST:~/$STAGED" --zone="$ZONE"

echo "→ ssh  install to $TARGET_DIR/index.html"
gcloud compute ssh "$HOST" --zone="$ZONE" --command="\
    sudo mkdir -p '$TARGET_DIR' && \
    sudo mv ~/'$STAGED' '$TARGET_DIR/index.html' && \
    sudo chown root:www-data '$TARGET_DIR/index.html' 2>/dev/null || true && \
    sudo chmod 644 '$TARGET_DIR/index.html'"

echo "✓ deployed → https://mihaicosma.com/diet/"
