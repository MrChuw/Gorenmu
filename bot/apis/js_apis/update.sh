#!/usr/bin/env bash

set -euo pipefail

LIBS=(
  "https://unpkg.com/mathjs@latest/lib/browser/math.js|math.js"
)

DEST_DIR="./"

for ENTRY in "${LIBS[@]}"; do
  URL="${ENTRY%%|*}"
  FILENAME="${ENTRY#*|}"
  TARGET_PATH="${DEST_DIR}${FILENAME}"

  if curl -sSL -o "${TARGET_PATH}" "${URL}"; then
    SIZE=$(wc -c < "${TARGET_PATH}" | tr -d ' ')
    if [ "$SIZE" -lt 500 ]; then
      echo "Saved file is too small: ${SIZE} bytes."
    else
      echo "${FILENAME}: download complete (${SIZE} bytes)"
    fi
  else
    echo "Error downloading: ${URL}"
  fi
done
