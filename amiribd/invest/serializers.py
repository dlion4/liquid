from rest_framework import serializers

from .models import Account
from .models import Plan
from .models import PlanType
from .models import Pool


class PlanTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanType
        fields = "__all__"


class PoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pool
        fields = "__all__"


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = "__all__"
