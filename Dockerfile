FROM mcr.microsoft.com/playwright/python:v1.60.0-jammy

# Show print() output immediately in the cron log
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Only the code goes in the image. Credentials come from .env at runtime (docker-compose.yml).
COPY main.py .

CMD ["python", "main.py"]
