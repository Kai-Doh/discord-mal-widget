#!/usr/bin/env bash

# Change to the script's own directory
cd "$(dirname "$0")" || exit 1

echo "Starting updates. Will run every 6 hours. Press Ctrl+C to stop, unless you disowned."

while true; do
    echo "[$(date)] Updating..."
    . ./venv/bin/activate
    python refresh_mal.py
    deactivate
    echo "[$(date)] Finished, sleeping for 6 hours."
    sleep 21600
done
