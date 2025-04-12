FROM python:3.12-slim

WORKDIR /app 

COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .
