# Warehouse Management System

A simple warehouse inventory management API built with Python, Flask, PostgreSQL and Docker.

## Features
- Add and list products
- Search products by name
- Receive and issue stock
- Prevent issuing more stock than available
- Health check endpoint
- Automated tests with pytest
- PostgreSQL database with persistent Docker volume
- GitHub Actions CI pipeline
- Database backup and restore scripts

## Run with Docker
1. Copy .env.example to .env and set secure credentials.
2. Run: docker compose up -d --build
3. Check: http://localhost:5000/health

## Run tests
python -m pytest -v

## API endpoints
- GET /products
- POST /products
- GET /products/search?name=...
- GET /products/<id>
- POST /products/<id>/receive
- POST /products/<id>/issue
- GET /health

## Database backup
Run the backup.sh script from Bash: ./backup.sh

## Database restore
Run: ./restore.sh backups/warehouse_backup.sql
