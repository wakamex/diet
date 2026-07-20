#!/bin/bash
# Deploy the /diet/ page on mihaicosma.com.
#
# Source:  ./site/index.html (colocated with the pipeline that generates data.json)
# Target:  mc-new:/var/www/mihaicosma.com/diet/index.html
#
# Only the /diet/ subfolder of the live site is touched — the rest of
# mihaicosma.com is left alone. data.json is served from jsDelivr. The deployed
# page is rewritten to use the exact current Git commit instead of mutable
# @main, preventing browsers and CDN edges from retaining an older dataset.

set -euo pipefail

SRC="$(dirname "$(realpath "$0")")/site/index.html"
REPO_DIR="$(dirname "$(realpath "$0")")"
ZONE="us-central1-a"
HOST="mc-new"
TARGET_DIR="/var/www/mihaicosma.com/diet"

if [ ! -f "$SRC" ]; then
    echo "ERROR: $SRC not found — nothing to deploy" >&2
    exit 1
fi

COMMIT="$(git -C "$REPO_DIR" rev-parse HEAD)"
LOCAL_STAGED="$(mktemp)"
REMOTE_STAGED="diet-index.${COMMIT}.html"
trap 'rm -f "$LOCAL_STAGED"' EXIT

sed "s|https://cdn.jsdelivr.net/gh/wakamex/diet@main/site|https://cdn.jsdelivr.net/gh/wakamex/diet@${COMMIT}/site|" \
    "$SRC" > "$LOCAL_STAGED"

if ! grep -q "diet@${COMMIT}/site" "$LOCAL_STAGED"; then
    echo "ERROR: failed to pin data URL to commit $COMMIT" >&2
    exit 1
fi

echo "→ scp  $SRC (data@$COMMIT) → $HOST:~/$REMOTE_STAGED"
gcloud compute scp "$LOCAL_STAGED" "$HOST:~/$REMOTE_STAGED" --zone="$ZONE"

echo "→ ssh  install to $TARGET_DIR/index.html"
gcloud compute ssh "$HOST" --zone="$ZONE" --command="\
    sudo mkdir -p '$TARGET_DIR' && \
    sudo mv ~/'$REMOTE_STAGED' '$TARGET_DIR/index.html' && \
    sudo chown root:www-data '$TARGET_DIR/index.html' 2>/dev/null || true && \
    sudo chmod 644 '$TARGET_DIR/index.html'"

echo "✓ deployed → https://mihaicosma.com/diet/"
