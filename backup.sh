#!/bin/bash
set -e
mkdir -p backups
source .env
echo 'Creating database backup...'
docker compose exec -T db pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB" > "backups/warehouse_$(date +%Y%m%d_%H%M%S).sql"
echo 'Backup completed successfully.'
