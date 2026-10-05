#!/bin/bash
PROJECT_DIR="/home/jeremytran/Project/Scheduler_TDC"
PYTHON="/home/jeremytran/Project/Scheduler_TDC/tutorbot-env/bin/python3"

# Set this to a Wednesday that starts your rotation.
# Example:
# Week 0 = Wednesday
# Week 1 = Thursday
# Week 2 = Friday
# Week 3 = Wednesday again
START_DATE="2026-07-01"

S3_BUCKET="s3://scheduler-tdc-logs-167552806929-us-east-1-an"

cd "$PROJECT_DIR"

DATE=$(date +%F)
LOGFILE="logs/cron-$DATE.log"
mkdir -p logs

TODAY_DOW=$(date +%u)
# Monday=1, Tuesday=2, Wednesday=3, Thursday=4, Friday=5
TODAY_SECONDS=$(date +%s)
START_SECONDS=$(date -d "$START_DATE" +%s)
DAYS_SINCE=$(( (TODAY_SECONDS - START_SECONDS) / 86400 ))
WEEKS_SINCE=$(( DAYS_SINCE / 7 ))
ROTATION=$(( WEEKS_SINCE % 3 ))

# Rotation:
# 0 = Wednesday
# 1 = Thursday
# 2 = Friday
if [ "$ROTATION" -eq 0 ]; then
    EXPECTED_DOW=3
elif [ "$ROTATION" -eq 1 ]; then
    EXPECTED_DOW=4
else
    EXPECTED_DOW=5
fi

echo "-----" >> "$LOGFILE"
echo "Cron check ran at $(date)" >> "$LOGFILE"
echo "Today DOW: $TODAY_DOW" >> "$LOGFILE"
echo "Weeks since start: $WEEKS_SINCE" >> "$LOGFILE"
echo "Rotation: $ROTATION" >> "$LOGFILE"
echo "Expected DOW: $EXPECTED_DOW" >> "$LOGFILE"

if [ "$TODAY_DOW" -eq "$EXPECTED_DOW" ]; then
    echo "Today is the assigned scheduling day. Running bot." >> "$LOGFILE"
    docker compose run --rm scheduler >> "$LOGFILE" 2>&1

    # --- Upload this run's log and screenshots to S3 ---
    aws s3 cp "$LOGFILE" "$S3_BUCKET/$DATE/cron.log" >> "$LOGFILE" 2>&1
    aws s3 sync screenshots/ "$S3_BUCKET/$DATE/screenshots/" >> "$LOGFILE" 2>&1
else
    echo "Today is not the assigned scheduling day. Skipping bot." >> "$LOGFILE"

fi
