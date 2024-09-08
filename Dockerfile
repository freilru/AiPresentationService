# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    libsqlite3-dev

# Создаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей и устанавливаем их
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта
COPY . /app/

# Запускаем миграции и собираем статику
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput


RUN pip install gunicorn
# Открываем порт
EXPOSE 8000

# Запускаем приложение
CMD ["gunicorn", "AiPresentationService.wsgi:application", "--bind", "0.0.0.0:8000"]
