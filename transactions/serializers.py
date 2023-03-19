from rest_framework import serializers
from .models import PaymentTransactionModel


class PaymentTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTransactionModel
        fields = '__all__'
