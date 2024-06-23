from django.db import models
from django.core.validators import FileExtensionValidator, EmailValidator
from django.contrib.auth.models import AbstractUser



class CustomUser(AbstractUser):
    email = models.CharField(max_length=40, unique=True, blank=False, null=False, validators=[EmailValidator(message="Email field is required")])
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
