from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser,Group,Permission

class User(AbstractUser):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    full_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20, unique=True)
    company_name = models.CharField(max_length=255)
    address = models.TextField()
    industry = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",
        help_text='The groups this user belongs to.',
        related_query_name='user'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user'
    )

    REQUIRED_FIELDS = ['email', 'full_name', 'contact_number', 'company_name', 'address', 'industry']

    def __str__(self):
        return self.username