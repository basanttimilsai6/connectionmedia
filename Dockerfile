FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=configurations.settings.dev
ENV DEBUG=False

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

# Copy project
COPY . /app/

# Collect static files
RUN python3 manage.py collectstatic --noinput
# Expose port 8000 for Django app
EXPOSE 8000

# Run the Django development server (change to gunicorn for production)
CMD ["gunicorn", "configurations.wsgi:application", "--bind", "0.0.0.0:8000"]
