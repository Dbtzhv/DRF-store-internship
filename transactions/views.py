from .serializers import PaymentTransactionSerializer
from .models import PaymentTransactionModel
from rest_framework import viewsets


class PaymentTransactionAPIView(viewsets.ModelViewSet):
    queryset = PaymentTransactionModel.objects.all()
    serializer_class = PaymentTransactionSerializer
