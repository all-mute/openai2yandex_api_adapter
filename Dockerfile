# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы в контейнер
COPY . /app/

# Устанавливаем FastAPI и Uvicorn
RUN pip install -r requirements.txt

EXPOSE 9041

ENV FOLDER_ID=""
ENV YANDEX_API_KEY=""

# healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl --fail http://localhost:9041/health || exit 1

# Команда для запуска приложения
CMD ["uvicorn", "main:main_app", "--host", "0.0.0.0", "--port", "9041"]
