# Используем легкий образ Python
FROM python:3.11-slim

# Отключаем буферизацию вывода (чтобы логи видеть сразу)
ENV PYTHONUNBUFFERED=1

# Рабочая папка внутри контейнера
WORKDIR /app

# Ставим зависимости системы (нужны для сборки некоторых python пакетов)
RUN apt-get update && apt-get install -y gcc libpq-dev

# Копируем файл зависимостей и устанавливаем их
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

# Копируем код проекта внутрь контейнера
COPY backend/ .