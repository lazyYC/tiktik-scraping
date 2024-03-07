FROM python:3.8-slim

# RUN apt-get update && apt-get install -y chromium-driver chromium && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y wget
# 下载 Google Chrome Stable
RUN wget -c https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

# 安装 Google Chrome
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb

# 清理操作
RUN apt-get clean && rm -rf /var/lib/apt/lists/* && rm google-chrome-stable_current_amd64.deb


WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENV CELERY_BROKER_URL=redis://redis:6379/0
ENV CELERY_RESULT_BACKEND=redis://redis:6379/0



