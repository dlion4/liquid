from django.contrib import admin
from .forms import PositionForm, AdminPlatformTypeForm
from .models import PlantformType, Position, Agent, Plantform
from unfold.admin import (
    ModelAdmin,
    StackedInline,
    TabularInline,
)

from .forms import AdminAgentForm

# Register your models here.


@admin.register(Position)
class PositionAdmin(ModelAdmin):
    list_display = ("name",)
    # form = PositionForm


class PlantformInline(StackedInline):
    model = Plantform
    extra = 1
    fields = [
        'plantform_type',
    ]
    


@admin.register(Agent)
class AgentAdmin(ModelAdmin):
    list_display = ("profile",)
    # form = AdminAgentForm


@admin.register(PlantformType)
class PlantformAdmin(ModelAdmin):
    list_display = ("name",)
    inlines = [PlantformInline]
    # form = AdminPlatformTypeForm
