from django.contrib import admin
from .models import PaymentTransactionModel
from django.db.models import QuerySet


@admin.register(PaymentTransactionModel)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')
    search_fields = ('id',)
    actions = ['decline_transaction', 'complete_transaction']

    @admin.action(description='Отклонить транзакцию')
    def decline_transaction(self, request, qs: QuerySet):
        qs.update(status='declined')
        self.message_user(request, 'Транзакция была отклонена')

    @admin.action(description='Подтвердить транзакцию')
    def complete_transaction(self, request, qs: QuerySet):
        qs.update(status='completed')
        self.message_user(request, 'Транзакция была подтверждена')
