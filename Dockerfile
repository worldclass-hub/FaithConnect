# Use official Python image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Optional collectstatic (don’t fail if it errors)
RUN python manage.py collectstatic --noinput || echo "collectstatic failed, ignoring..."

# Run app
CMD gunicorn doxcela.wsgi:application --bind 0.0.0.0:$PORT
