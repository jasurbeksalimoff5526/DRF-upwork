from django.db import models
from django.conf import settings
# Create your models here.


class Notification(models.Model):
    class NotificationType(models.TextChoices):
        NEW_BID = "NEW_BID", "New bid"
        BID_ACCEPTED = "BID_ACCEPTED", "Bid accepted"
        BID_REJECTED = "BID_REJECTED", "Bid rejected"
        CONTRACT_CREATED = "CONTRACT_CREATED", "Contract created"
        PAYMENT_PENDING = "PAYMENT_PENDING", "Payment pending"
        PAYMENT_COMPLETED = "PAYMENT_COMPLETED", "Payment completed"
        PROJECT_STARTED = "PROJECT_STARTED", "Project started"
        PROJECT_COMPLETED = "PROJECT_COMPLETED", "Project completed"
        CONTRACT_FINISHED = "CONTRACT_FINISHED", "Contract finished"
        REVIEW_CREATED = "REVIEW_CREATED", "Review created"
        DEADLINE_WARNING = "DEADLINE_WARNING", "Deadline warning"
        MESSAGE_RECEIVED = "MESSAGE_RECEIVED", "Message received"

    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sent_notifications"
    )

    notification_type = models.CharField(
        max_length=50,
        choices=NotificationType.choices
    )

    title = models.CharField(max_length=255)
    message = models.TextField()

    project = models.ForeignKey(
        "project.Project",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notifications"
    )

    contract = models.ForeignKey(
        "contract.Contract",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notifications"
    )

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.receiver} - {self.notification_type}"
