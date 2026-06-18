# Scheduler_TDC

A Python + Playwright automation project for opening Tutor.com, logging in, navigating to the Schedule Manager, and selecting scheduling hours.

## Goals

* Open Tutor.com provider schedule page
* Log in using credentials from a local `.env` file
* Open Schedule Manager
* Select desired schedule cells
* Submit selected hours
* Eventually add better error handling, unavailable-cell detection, and scheduled execution

## Requirements

* Python
* Playwright
* python-dotenv

## Environment Variables

Create a local `.env` file:

```env
TUTOR_EMAIL=your_email_here
TUTOR_PASSWORD=your_password_here
```

Do not commit `.env` to GitHub.

---

## Setup

### Clone Repo

```bash
git clone https://github.com/JeremyTran211/Scheduler_TDC.git
cd Scheduler_TDC
```

---

## Mac Commands

### Create Virtual Environment

```bash
python3 -m venv tutorbot-env
```

### Activate Virtual Environment

```bash
source tutorbot-env/bin/activate
```

### Deactivate Virtual Environment

```bash
deactivate
```

### Install Dependencies

```bash
python3 -m pip install -r requirements.txt
```

### Install Playwright Chromium Browser

```bash
python3 -m playwright install chromium
```

### Create `.env`

```bash
nano .env
```

### Run Program

```bash
python3 main.py
```

### Generate Playwright Code

```bash
python3 -m playwright codegen https://www.tutor.com/providers/schedule
```

---

## Windows Commands

### Create Virtual Environment

```powershell
python -m venv tutorbot-env
```

### Activate Virtual Environment

Command Prompt:

```bat
tutorbot-env\Scripts\activate
```

PowerShell:

```powershell
.\tutorbot-env\Scripts\Activate.ps1
```

### Deactivate Virtual Environment

```powershell
deactivate
```

### Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

### Install Playwright Chromium Browser

```powershell
python -m playwright install chromium
```

### Create `.env`

```powershell
notepad .env
```

### Run Program

```powershell
python main.py
```

### Generate Playwright Code

```powershell
python -m playwright codegen https://www.tutor.com/providers/schedule
```

---

## Updating Dependencies

After installing new packages, update `requirements.txt`.

Mac:

```bash
python3 -m pip freeze > requirements.txt
```

Windows:

```powershell
python -m pip freeze > requirements.txt
```

---

## Git Commands

Check status:

```bash
git status
```

Add files:

```bash
git add .
```

Commit changes:

```bash
git commit -m "Your message"
```

Push changes:

```bash
git push
```

Pull latest changes:

```bash
git pull
```

---

## Do Not Commit

Make sure `.gitignore` includes:

```gitignore
.env
tutorbot-env/
__pycache__/
*.pyc
*.log
*.png
```
