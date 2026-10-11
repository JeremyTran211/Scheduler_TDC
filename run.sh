#!/bin/bash
# Runs the Tutor.com scheduler, then ships the log and screenshots to S3.
# cron decides which day it runs (see hosts/pi/crontab in the Homelab repo).
#
# Exit code is the bot's exit code (0 ok, 1 failed, 2 hours not scheduled).
#
# Test without booking anything:  DRY_RUN=1 ./run.sh

# Work from this script's folder no matter where cron calls it from
APP_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$APP_DIR" || exit 1

# Delete local logs/screenshots older than this; S3 keeps the copies
KEEP_DAYS=30

# Bucket lives in .env so the AWS account ID isn't published in the repo.
# Read just this one key: sourcing .env could break on special characters in the password.
S3_BUCKET="$(grep -E '^S3_BUCKET=' .env 2>/dev/null | cut -d= -f2- | tr -d '"'"'"'\r')"

DATE=$(date +%F)
LOGFILE="logs/cron-$DATE.log"
mkdir -p logs screenshots

echo "-----" >> "$LOGFILE"
echo "Cron check ran at $(date)" >> "$LOGFILE"

if [ "$DRY_RUN" = "1" ]; then
    echo "DRY_RUN=1: not running the bot or uploading." >> "$LOGFILE"
    echo "S3_BUCKET set: $([ -n "$S3_BUCKET" ] && echo yes || echo NO)" >> "$LOGFILE"
    exit 0
fi

echo "Running bot." >> "$LOGFILE"
docker compose run --rm -T -e RUN_DATE="$DATE" scheduler >> "$LOGFILE" 2>&1
STATUS=$?
echo "Bot exit code: $STATUS" >> "$LOGFILE"

# --- Upload this run's log and screenshots to S3 ---
if [ -n "$S3_BUCKET" ]; then
    aws s3 cp "$LOGFILE" "$S3_BUCKET/$DATE/cron.log" >> "$LOGFILE" 2>&1
    if [ -d "screenshots/$DATE" ]; then
        aws s3 sync "screenshots/$DATE/" "$S3_BUCKET/$DATE/screenshots/" >> "$LOGFILE" 2>&1
    fi
else
    echo "S3_BUCKET not set in .env. Skipping upload." >> "$LOGFILE"
fi

# --- Local cleanup ---
find logs -name 'cron-*.log' -mtime +"$KEEP_DAYS" -delete
find screenshots -mindepth 1 -maxdepth 1 -type d -mtime +"$KEEP_DAYS" -exec rm -rf {} +

exit "$STATUS"
