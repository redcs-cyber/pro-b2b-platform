#!/usr/bin/env bash
set -euo pipefail

python scripts/vercel_deploy_check.py

if ! command -v vercel >/dev/null 2>&1; then
  echo "Vercel CLI bulunamadı. Kurulum: npm i -g vercel" >&2
  exit 2
fi

: "${VERCEL_ORG_ID:?VERCEL_ORG_ID zorunlu}"
: "${VERCEL_PROJECT_ID:?VERCEL_PROJECT_ID zorunlu}"

vercel pull --yes --environment=production
vercel build --prod
vercel deploy --prebuilt --prod
