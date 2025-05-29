from django.db import models
import uuid
# Create your models here.


class Organization(models.Model):
    inn = models.CharField(max_length=12, unique=True)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return f"Organization INN: {self.inn}, Balance: {self.balance}"

class Payment(models.Model):
    operation_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    payer_inn = models.CharField(max_length=12)
    document_number = models.CharField(max_length=50)
    document_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment ID: {self.operation_id}, Amount: {self.amount}, Payer INN: {self.payer_inn}"

class BalanceLog(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    previous_balance = models.DecimalField(max_digits=15, decimal_places=2)
    new_balance = models.DecimalField(max_digits=15, decimal_places=2)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"BalanceLog for organization with INN {self.organization.inn}: "
            f"{self.previous_balance} -> {self.new_balance} (Payment ID: {self.payment.operation_id})"
            )