from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from accounts.models import CustomUser
from shared.models import BaseModel


OPEN, IN_PROGRESS, COMPLETED, CANCELLED = ("open", "in_progress", "completed", "cancelled")


class Project(BaseModel):
    STATUS_CHOICES = (
        (OPEN, OPEN),
        (IN_PROGRESS, IN_PROGRESS),
        (COMPLETED, COMPLETED),
        (CANCELLED, CANCELLED),
    )

    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="projects")
    title = models.CharField(max_length=255)
    description = models.TextField()
    budget = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    deadline = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=OPEN)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
