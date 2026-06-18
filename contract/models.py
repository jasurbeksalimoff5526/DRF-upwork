from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from accounts.models import CustomUser
from project.models import COMPLETED, IN_PROGRESS, OPEN, Project
from shared.models import BaseModel


PENDING, ACCEPTED, REJECTED = ("pending", "accepted", "rejected")
ACTIVE, FINISHED, CANCELLED = ("active", "finished", "cancelled")


class Bid(BaseModel):
    STATUS_CHOICES = (
        (PENDING, PENDING),
        (ACCEPTED, ACCEPTED),
        (REJECTED, REJECTED),
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="bids")
    freelancer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="bids")
    price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["project", "freelancer"], name="unique_bid_per_project_freelancer")
        ]

    def __str__(self):
        return f"{self.freelancer} -> {self.project}"


class Contract(BaseModel):
    STATUS_CHOICES = (
        (ACTIVE, ACTIVE),
        (FINISHED, FINISHED),
        (CANCELLED, CANCELLED),
    )

    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name="contract")
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="client_contracts")
    freelancer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="freelancer_contracts")
    agreed_price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ACTIVE)
    finished_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.project} - {self.freelancer}"

    def finish(self):
        self.status = FINISHED
        self.finished_at = timezone.now()
        self.save(update_fields=["status", "finished_at", "updated_at"])

        self.project.status = COMPLETED
        self.project.save(update_fields=["status", "updated_at"])


class Review(BaseModel):
    contract = models.OneToOneField(Contract, on_delete=models.CASCADE, related_name="review")
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.contract.freelancer} rating: {self.rating}"
