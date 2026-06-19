from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator

from accounts.models import CustomUser
from shared.models import BaseModel


DEPOSIT, WITHDRAW, ESCROW_HOLD, ESCROW_RELEASE, ESCROW_REFUND = (
    "deposit",
    "withdraw",
    "escrow_hold",
    "escrow_release",
    "escrow_refund",
)

PENDING, COMPLETED, FAILED, CANCELLED = (
    "pending",
    "completed",
    "failed",
    "cancelled",
)


class Wallet(BaseModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="wallet")
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    frozen_balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))

    def __str__(self):
        return f"{self.user.username}'s Wallet - Balance: {self.balance}, Frozen: {self.frozen_balance}"


class Transaction(BaseModel):
    TRANSACTION_TYPE_CHOICES = (
        (DEPOSIT, "Deposit"),
        (WITHDRAW, "Withdraw"),
        (ESCROW_HOLD, "Escrow Hold"),
        (ESCROW_RELEASE, "Escrow Release"),
        (ESCROW_REFUND, "Escrow Refund"),
    )

    STATUS_CHOICES = (
        (PENDING, "Pending"),
        (COMPLETED, "Completed"),
        (FAILED, "Failed"),
        (CANCELLED, "Cancelled"),
    )

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="transactions")
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    
    # Optional fields for specific transactions
    card_number = models.CharField(max_length=20, blank=True)
    receipt_image = models.ImageField(upload_to="receipts/", blank=True, null=True)
    contract = models.ForeignKey('contract.Contract', on_delete=models.SET_NULL, null=True, blank=True, related_name="transactions")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} ({self.status}) for {self.wallet.user.username}"
