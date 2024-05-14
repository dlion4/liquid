from django.contrib import admin
from .models import PlantformType, Position, Agent, Plantform

# Register your models here.


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("name",)


class PlantformInline(admin.StackedInline):
    model = Plantform
    extra = 0


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ("profile",)


@admin.register(PlantformType)
class PlantformAdmin(admin.ModelAdmin):
    list_display = ("name",)
