from django.contrib import admin
from .models import Payment, Organization, BalanceLog

# Register your models here.

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = 'pk', 'operation_id', 'amount', 'payer_inn', 'document_number', 'document_date', 'created_at',

@admin.register(Organization)
class PaymentAdmin(admin.ModelAdmin):
    list_display = 'pk', 'inn', 'balance',

@admin.register(BalanceLog)
class PaymentAdmin(admin.ModelAdmin):
    list_display = 'pk', 'organization', 'previous_balance','new_balance', 'payment', 'created_at',


