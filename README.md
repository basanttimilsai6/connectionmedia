# connectionmedia
ConnectionMedia is a Django REST API project with JWT-based auth, user registration, connection requests, and async notifications using Celery. Features include user search, secure login, and modular structure for scalability.

# 🚀 Django DRF Social Connection Platform (Dockerized)

This project is a Django REST Framework (DRF)-based backend service for user registration, login (JWT), connection management, and real-time notifications using Celery + Redis. The app is fully containerized using **Docker Compose**.

---

## 📦 Features

- ✅ JWT Authentication (15-minute expiry)
- ✅ User Registration
- ✅ Connection Request Handling (Send/Accept/Reject)
- ✅ Asynchronous Notifications via Celery
- ✅ Swagger/OpenAPI Documentation
- ✅ Docker + PostgreSQL + Redis setup

---
## 🐳 How to Run the Project with Docker Compose

### 1. Clone the Repository

```bash
https://github.com/basanttimilsai6/connectionmedia.git
cd connectionmedia
```

## Create .env (nano .env)
```bash
DEBUG=1
POSTGRES_NAME =  f1
POSTGRES_USER = soft
POSTGRES_PASSWORD = soft
POSTGRES_HOST = db
POSTGRES_PORT = 5432
CELERY_BROKER_URL=redis://redis:6379/0
SECRET_KEY = 'django-insecure-ASDFGHJ34567DFGHJ2345CVBNM34567XCVBNMCVBN'
ACCESS_TOKEN_LIFETIME = 15
REFRESH_TOKEN_LIFETIME = 1
```
```bash
docker-compose build
docker-compose up

docker exec -it web-container-name bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic (in case of staticfiles folder not created)
```

## Swagger URL
[Swagger URL](http://localhost:8000/api/schema/swagger-ui/)

## Admin URL
http://localhost:8000/admin/

