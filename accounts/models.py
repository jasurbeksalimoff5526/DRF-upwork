from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

from shared.models import BaseModel


CLIENT, FREELANCER = ("client", "freelancer")


class CustomUser(AbstractUser, BaseModel):
    ROLE_CHOICES = (
        (CLIENT, CLIENT),
        (FREELANCER, FREELANCER),
    )

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=CLIENT)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.username

    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }

    @property
    def is_client(self):
        return self.role == CLIENT

    @property
    def is_freelancer(self):
        return self.role == FREELANCER
