#!/bin/bash
set -e
if [ -z "$1" ]; then echo 'Usage: ./restore.sh backups/file.sql'; exit 1; fi
source .env
echo 'Restoring database...'
docker compose exec -T db psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" < "$1"
echo 'Restore completed successfully.'
