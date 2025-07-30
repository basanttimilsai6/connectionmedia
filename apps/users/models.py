from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,BaseUserManager



class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The username is required.")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not password:
            raise ValueError("Superuser must have a password.")
        if not username:
            raise ValueError("Superuser must have a username.")
        return self.create_user(username=username, password=password, **extra_fields)

    

class User(AbstractBaseUser, PermissionsMixin):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    full_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20, unique=True)
    company_name = models.CharField(max_length=255)
    address = models.TextField()
    industry = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['username'], name='unique_username'),
            models.UniqueConstraint(fields=['email'], name='unique_email'),
            models.UniqueConstraint(fields=['contact_number'], name='unique_contact_number'),
        ]

    def __str__(self):
        return self.username