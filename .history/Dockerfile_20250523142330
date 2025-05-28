FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TZ=Asia/Seoul

WORKDIR /app

# ✅ 이 경로에서 manage.py, config 등 전부 복사됨
COPY . /app

RUN apt-get update && apt-get install -y \
    tzdata \
    netcat-openbsd \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# ✅ config.asgi 기준으로 실행
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "config.asgi:application"]
