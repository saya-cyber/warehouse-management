#!/bin/bash
set -e
echo 'Deploying Warehouse Management System...'
docker compose up -d --build
echo 'Deployment completed successfully.'
