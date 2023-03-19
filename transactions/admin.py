from django.contrib import admin
from .models import PaymentTransactionModel


@admin.register(PaymentTransactionModel)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')
    search_fields = ('id',)
