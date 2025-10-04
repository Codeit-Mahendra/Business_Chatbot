
# FROM python:3.10-slim-buster

# WORKDIR /app

# COPY . /app

# RUN pip install -r requirements.txt

# CMD ["python3", "app.py"]

# Use slim image to save space
FROM python:3.9-slim

# Install only what you need
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code (respects .dockerignore)
COPY . .

CMD ["python", "app.py"]
