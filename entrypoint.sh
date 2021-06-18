#!/bin/sh

set -e

if [ -n "$CF_API_KEY_FILE" ]; then export CF_API_KEY="$(cat $CF_API_KEY_FILE)"; fi

exec "$@"
