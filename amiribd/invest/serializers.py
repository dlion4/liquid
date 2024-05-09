from rest_framework import serializers


from .models import PlanType



class PlanTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanType
        fields = "__all__"

