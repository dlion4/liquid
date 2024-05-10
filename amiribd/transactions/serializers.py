from .models import Transaction
from rest_framework import serializers


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "type",
            "created_at",
            "amount",
            "source",
        ]
