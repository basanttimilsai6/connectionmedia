FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=configurations.settings.dev

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Accept build args for sensitive envs
ARG DEBUG
ARG SECRET_KEY
ARG POSTGRES_NAME
ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG POSTGRES_HOST
ARG POSTGRES_PORT
ARG CELERY_BROKER_URL
ARG ACCESS_TOKEN_LIFETIME
ARG REFRESH_TOKEN_LIFETIME

# Set them as environment variables inside the container
ENV DEBUG=$DEBUG
ENV SECRET_KEY=$SECRET_KEY
ENV POSTGRES_NAME=$POSTGRES_NAME
ENV POSTGRES_USER=$POSTGRES_USER
ENV POSTGRES_PASSWORD=$POSTGRES_PASSWORD
ENV POSTGRES_HOST=$POSTGRES_HOST
ENV POSTGRES_PORT=$POSTGRES_PORT
ENV CELERY_BROKER_URL=$CELERY_BROKER_URL
ENV ACCESS_TOKEN_LIFETIME=$ACCESS_TOKEN_LIFETIME
ENV REFRESH_TOKEN_LIFETIME=$REFRESH_TOKEN_LIFETIME

# Copy project
COPY . /app/

# Collect static files
# RUN python3 manage.py collectstatic --noinput

# Expose port 8000
EXPOSE 8000

# Run Django with Gunicorn
CMD ["gunicorn", "configurations.wsgi:application", "--bind", "0.0.0.0:8000"]
