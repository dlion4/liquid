from rest_framework import serializers
from .models import PaystackPaymentStatus


class PaystackPaymentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaystackPaymentStatus
        fields = "__all__"