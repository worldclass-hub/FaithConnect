/Users/mac/Desktop/doxcela/doxcela/Dockerfile


# Use official Python slim image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory inside container
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

# Copy project files to container
COPY . .

# Run migrations, collect static files, and start Gunicorn on Railway-assigned $PORT
CMD bash -c "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn doxcela.wsgi:application --bind 0.0.0.0:$PORT"
