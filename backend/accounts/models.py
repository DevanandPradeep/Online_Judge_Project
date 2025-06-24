from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'  # or 'email' if you prefer
    REQUIRED_FIELDS = ['email', 'full_name']

    def __str__(self):
        return self.username
