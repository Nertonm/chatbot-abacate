#!/bin/bash
set -e

# Load env variables from .env if present, but do not override existing env vars
if [ -f ".env" ]; then
  echo "Loading .env (without overwriting existing env vars)"
  # read line by line, skip comments and empty lines
  while IFS='=' read -r key value; do
    # skip blanks or comments
    [[ "$key" =~ ^# ]] && continue
    [[ -z "$key" ]] && continue
    # trim possible surrounding whitespace
    key=$(echo "$key" | xargs)
    # remove possible quotes around value
    value=$(echo "$value" | sed -e 's/^"//' -e 's/"$//' -e "s/^'//" -e "s/'$//")
    # only export if not already set
    if [ -z "${!key}" ]; then
      export "$key=$value"
    fi
  done < <(grep -v '^#' .env | sed '/^$/d')
fi

SCRIPT_DIR=$(dirname "$0")

echo "Starting entrypoint: waiting for DB..."
echo "Using DB host: ${DB_HOST:-db}, port: ${DB_PORT:-3306}"
${SCRIPT_DIR}/wait-for-db.sh

echo "Starting application: $@"
exec "$@"
