from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        FARMER = "farmer", "Farmer"
        EXTENSION_AGENT = "extension_agent", "Extension Agent"
        INSTITUTION_ADMIN = "institution_admin", "Institution Admin"
        ADMIN = "admin", "Platform Admin"

    role = models.CharField(max_length=32, choices=Role.choices, default=Role.FARMER)
    phone_number = models.CharField(max_length=20, blank=True, db_index=True)
    preferred_language = models.CharField(max_length=10, default="en")
    organization = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.username
