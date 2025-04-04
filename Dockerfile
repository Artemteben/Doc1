FROM python:3.12-slim


# Установить зависимости Python
WORKDIR /app

COPY /requirements.txt /

RUN pip install -r /requirements.txt --no-cache-dir

# Скопировать исходный код
COPY . .
