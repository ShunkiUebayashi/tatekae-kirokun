from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    secret_question = models.CharField(max_length=255)
    secret_answer = models.CharField(max_length=255)


class PendingInvoice(models.Model):
    sender = models.ForeignKey(CustomUser, related_name="sent_pending_invoices", on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name="received_pending_invoices", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)  # フィールドを追加


class ApprovedInvoice(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="sent_approved_invoices", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="received_approved_invoices", on_delete=models.CASCADE
    )
    amount = models.PositiveIntegerField()  # PositiveIntegerFieldで1以上の整数のみを許可
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)  # フィールドを追加

    def __str__(self):
        return f"Invoice from {self.sender} to {self.receiver} - Amount: {self.amount}"