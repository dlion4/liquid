from django.contrib import admin
from django_celery_beat.admin import ClockedScheduleAdmin as BaseClockedScheduleAdmin
from django_celery_beat.admin import CrontabScheduleAdmin as BaseCrontabScheduleAdmin
from django_celery_beat.admin import PeriodicTaskAdmin as BasePeriodicTaskAdmin
from django_celery_beat.admin import PeriodicTaskForm
from django_celery_beat.admin import TaskSelectWidget
from django_celery_beat.models import ClockedSchedule
from django_celery_beat.models import CrontabSchedule
from django_celery_beat.models import IntervalSchedule
from django_celery_beat.models import PeriodicTask
from django_celery_beat.models import SolarSchedule
from unfold.admin import ModelAdmin
from unfold.admin import UnfoldAdminSelectWidget
from unfold.contrib.forms.widgets import UnfoldAdminTextInputWidget
from unfold.contrib.forms.widgets import WysiwygWidget
from unfold.widgets import UnfoldAdminEmailInputWidget

from amiribd.core.admin import earnkraft_site

from .models import AdminSendMail
from .models import AdminSendMailCategory
from .models import CompanyTermsAndPolicy
from .models import Contact

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


@admin.register(Contact, site=earnkraft_site)
class ContactAdmin(ModelAdmin):
    list_display = [
        "name",
        "email",
        "subject",
        "message",
    ]
    formfield_overrides = {
        "name": {"widget": UnfoldAdminTextInputWidget()},
        "email": {"widget": UnfoldAdminEmailInputWidget()},
        "subject": {"widget": UnfoldAdminTextInputWidget()},
        "message": {"widget": WysiwygWidget()},
    }

@admin.register(CompanyTermsAndPolicy, site=earnkraft_site)
class CompanyTermsAndPolicyAdmin(ModelAdmin):
    list_display = [
        "file",
        "created_at",
        "updated_at",
    ]


@admin.register(AdminSendMailCategory)
class AdminSendMailCategoryModelAdmin(ModelAdmin):
    list_display = ["name"]

@admin.register(AdminSendMail)
class AdminSendMailModelAdmin(ModelAdmin):
    list_display = [
        "category",
        "subject",
        "sent_at",
    ]
    formfield_overrides = {
        "message": {"widget": WysiwygWidget()},
    }

