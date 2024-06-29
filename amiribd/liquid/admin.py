from django.contrib import admin

from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import UnfoldAdminTextInputWidget
from django_celery_beat.models import (
    ClockedSchedule,
    CrontabSchedule,
    IntervalSchedule,
    PeriodicTask,
    SolarSchedule,
)
from unfold.widgets import UnfoldAdminEmailInputWidget
from unfold.contrib.forms.widgets import ArrayWidget, WysiwygWidget
from unfold.admin import UnfoldAdminSelectWidget
from django_celery_beat.admin import ClockedScheduleAdmin as BaseClockedScheduleAdmin
from django_celery_beat.admin import CrontabScheduleAdmin as BaseCrontabScheduleAdmin
from django_celery_beat.admin import PeriodicTaskAdmin as BasePeriodicTaskAdmin
from django_celery_beat.admin import PeriodicTaskForm, TaskSelectWidget

admin.site.unregister(PeriodicTask)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)


class UnfoldTaskSelectWidget(UnfoldAdminSelectWidget, TaskSelectWidget):
    pass


class UnfoldPeriodicTaskForm(PeriodicTaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["task"].widget = UnfoldAdminTextInputWidget()
        self.fields["regtask"].widget = UnfoldTaskSelectWidget()


@admin.register(PeriodicTask)
class PeriodicTaskAdmin(BasePeriodicTaskAdmin, ModelAdmin):
    form = UnfoldPeriodicTaskForm


@admin.register(IntervalSchedule)
class IntervalScheduleAdmin(ModelAdmin):
    pass


@admin.register(CrontabSchedule)
class CrontabScheduleAdmin(BaseCrontabScheduleAdmin, ModelAdmin):
    pass


@admin.register(SolarSchedule)
class SolarScheduleAdmin(ModelAdmin):
    pass

@admin.register(ClockedSchedule)
class ClockedScheduleAdmin(BaseClockedScheduleAdmin, ModelAdmin):
    pass


from .models import CompanyTermsAndPolicy, Contact
from amiribd.core.admin import earnkraft_site

@admin.register(Contact, site=earnkraft_site)
class ContactAdmin(ModelAdmin):
    list_display = [
        "name",
        "email",
        "subject",
        "message",
    ]
    formfield_overrides = {
        'name': {'widget': UnfoldAdminTextInputWidget()},
        'email': {'widget': UnfoldAdminEmailInputWidget()},
        'subject': {'widget': UnfoldAdminTextInputWidget()},
        'message': {'widget': WysiwygWidget()}
    }

@admin.register(CompanyTermsAndPolicy, site=earnkraft_site)
class CompanyTermsAndPolicyAdmin(ModelAdmin):
    list_display = [
        'file',
        'created_at',
        'updated_at',
    ]