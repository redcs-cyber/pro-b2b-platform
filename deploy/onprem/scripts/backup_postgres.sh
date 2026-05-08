#!/usr/bin/env bash
set -euo pipefail
BACKUP_DIR=${BACKUP_DIR:-/backups/prob2b}
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
mkdir -p "$BACKUP_DIR"
pg_dump "$DATABASE_URL" | gzip > "$BACKUP_DIR/prob2b_$STAMP.sql.gz"
find "$BACKUP_DIR" -type f -name 'prob2b_*.sql.gz' -mtime +14 -delete
