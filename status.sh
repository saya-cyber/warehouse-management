#!/bin/bash
echo 'Container status:'
docker compose ps
echo 'Container resource usage:'
docker stats --no-stream
