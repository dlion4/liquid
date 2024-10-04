# import easy audit models for deletion after db backup

from easyaudit.models import CRUDEvent, LoginEvent, RequestEvent


# import the schuldrs fro taking the backup

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import (
    DjangoMemoryJobStore,
    DjangoJobStore,
    register_events,
)

from django.core.management import call_command

import contextlib

# create a backup class


class Backup:
    SECONDS_PER_MINUTE = 60
    MINUTES_PER_HOUR = 60
    HOURS_PER_DAY = 24
    DAYS_PER_WEEK = 7
    WEEKS_PER_MONTH = 4  # Assuming 4 weeks per month for simplicity

    def call_db_backup(self):
        with contextlib.suppress(Exception):
            call_command("dbbackup")

    def call_delete_easyaudit_logs(self):
        with contextlib.suppress(Exception):
            CRUDEvent.objects.all().delete()
            LoginEvent.objects.all().delete()
            RequestEvent.objects.all().delete()

    def call_backup(self):
        scheduler = BackgroundScheduler()

        monthly_interval = (
            self.SECONDS_PER_MINUTE
            * self.MINUTES_PER_HOUR
            * self.HOURS_PER_DAY
            * self.DAYS_PER_WEEK
            * self.WEEKS_PER_MONTH
        )

        scheduler.add_jobstore(DjangoMemoryJobStore(), "kwasa")
        scheduler.add_job(
            self.call_db_backup,
            "interval",
            seconds=monthly_interval,
            id="db_backup",
            replace_existing=True,
        )
        scheduler.add_job(
            self.call_delete_easyaudit_logs,
            "interval",
            seconds=monthly_interval,
            id="delete_easyaudit_logs",
            replace_existing=True,
        )
        register_events(scheduler)
        scheduler.start()
        # scheduler.shutdown(wait=False)


def main():
    backup = Backup()
    backup.call_backup()
