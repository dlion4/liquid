from ninja import ModelSchema

from .models import PlanType


class PlanTypeSchema(ModelSchema):
    class Meta:
        model = PlanType
        fields = "__all__"
