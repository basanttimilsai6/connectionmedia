from configurations.settings.base import *
import os

SECRET_KEY = os.getenv("SECRET_KEY","django-insecure-ASDFGHJ34567DFGHJ2345CVBNM34567XCVBNMCVBN")

DEBUG = os.getenv("DEBUG", "0") == "1"

ALLOWED_HOSTS = ["*"]

POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_NAME","f1"),
        "USER": os.getenv("POSTGRES_USER","soft"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD","soft"),
        "HOST": os.getenv("POSTGRES_HOST","db"),
        "PORT": int(POSTGRES_PORT) if POSTGRES_PORT.isdigit() else 5432,
    }
}