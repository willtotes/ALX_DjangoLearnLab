from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_api_user = models.BooleanField(default=False)

    def __str__(self):
        return self.username
        
