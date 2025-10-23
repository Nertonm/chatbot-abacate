#!/bin/bash
set -e

# Wait for MySQL to be reachable
host="${DB_HOST:-db}"
port="${DB_PORT:-3306}"
user="${DB_USER:-root}"
pass="${DB_PASSWORD:-}"

echo "Waiting for DB at ${host}:${port}..."
# Use a simple TCP probe via bash /dev/tcp to avoid installing mysql client in the image
while ! (echo > /dev/tcp/${host}/${port}) >/dev/null 2>&1; do
  >&2 echo "DB ${host}:${port} is unavailable - sleeping"
  sleep 2
done

echo "DB ${host}:${port} is up - continuing"
