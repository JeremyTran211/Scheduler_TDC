# Scheduler_TDC

A Playwright bot that books my weekly Tutor.com hours. It logs in, opens the Schedule Manager,
jumps to next week, selects the configured hours, submits them, then reloads the page
to verify they were booked.

It runs on my homelab: a Raspberry Pi with Docker, started by cron every Wednesday at 9:01am.
How it's deployed there (host, schedule, secrets) is documented in the
[Homelab repo](https://github.com/JeremyTran211/Homelab).

## Files

| File | Purpose |
|---|---|
| `main.py` | The bot |
| `run.sh` | Entry point for cron: runs the container, uploads the log and screenshots to S3, prunes old files |
| `Dockerfile`, `docker-compose.yml` | Image built on Playwright's Python image; `.env`, `logs/` and `screenshots/` mounted at runtime |
| `.env.example` | Template for the real `.env` (never committed) |

## Configuration (`.env`)

| Variable | Meaning |
|---|---|
| `TUTOR_EMAIL`, `TUTOR_PASSWORD` | Tutor.com login |
| `S3_BUCKET` | `s3://bucket-name` for logs and screenshots |
| `SCHEDULE` | `regular` (Wed 6–9pm, Thu 7–9pm) or `sunday` (Sun 11am–4pm) |

Cell IDs follow `day + 7 × hour` (Sunday = 0, hours counted from 12am Eastern). They're listed in `main.py`.

## Exit codes

| Code | Meaning |
|---|---|
| 0 | All hours booked (or already booked) |
| 1 | Error: login, timeout, missing config |
| 2 | Ran, but some hours aren't booked. Check `verification_mismatch.png`. |

## Run it

```bash
cp .env.example .env && nano .env
docker compose build
DRY_RUN=1 ./run.sh                    # check paths and .env without booking anything
./run.sh                              # what cron runs (really books hours)
docker compose run --rm scheduler     # just the bot, no upload (really books hours)
```

Output goes to `logs/` and `screenshots/<date>/`. Both are gitignored.

After each run, `run.sh` also writes `/srv/status/scheduler-tdc.json` (last run, exit code, S3 upload
result) for the homelab dashboard. Set `STATUS_DIR` to write it somewhere else.

### Local development (Mac/Windows)

```bash
python3 -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m playwright install chromium
python main.py
python -m playwright codegen https://www.tutor.com/providers/schedule   # record selectors
```
