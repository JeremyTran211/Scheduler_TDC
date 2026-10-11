# CLAUDE.md

Notes for Claude Code when working in this repo.

## What this is

A Playwright bot that books my Tutor.com hours every Wednesday. It's an app that runs on my
homelab. Where and when it runs (the Pi, cron, secrets, AWS access) is defined in the
[Homelab repo](https://github.com/JeremyTran211/Homelab), not here. I'm learning as I go,
so explain changes in plain terms.

The repo is **public**.

## Rules

- **Never commit secrets or personal infrastructure details.** That includes `.env`, AWS keys,
  the S3 bucket name and the AWS account ID. Add new settings to `.env.example` with placeholder values.
- **Work on a branch and never push to `main`.** I review and merge through PRs.
- **Make changes in small steps and explain each one.**
- **Don't commit runtime output** (`logs/`, `screenshots/`).

## Careful

- **Running the bot for real books real Tutor.com hours.** Never run `main.py`, `run.sh` or
  `docker compose run scheduler` against the real site to test. Use `DRY_RUN=1 ./run.sh`,
  missing credentials, or a fake local page.
- Keep the exit codes. cron and the homelab's alerts depend on them:
  0 = booked, 1 = error, 2 = some hours not booked.
- The Dockerfile's Playwright image tag and `playwright` in `requirements.txt` must stay on the same version.
- It runs on a Raspberry Pi (ARM64), so the image must work on `linux/arm64`.

## Testing changes

- `python3 -m py_compile main.py`, then run it with missing credentials (expect exit 1), or
  against a fake local copy of the Schedule Manager page.
- `bash -n run.sh`, then `DRY_RUN=1 ./run.sh`.
- Anything that needs the Pi or the real site: list the exact commands and expected output in the PR.
