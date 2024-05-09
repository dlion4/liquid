from ninja import Schema, NinjaAPI, ModelSchema

from .models import PlanType


class PlanTypeSchema(ModelSchema):
    class Meta:
        model = PlanType
        fields = "__all__"
