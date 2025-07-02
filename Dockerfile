FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

WORKDIR /app

# Install system packages
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

# Run migrations, collect static, then start server with longer timeout & more workers
CMD bash -c "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn doxcela.wsgi:application --bind 0.0.0.0:$PORT --timeout 120 --workers 3"
