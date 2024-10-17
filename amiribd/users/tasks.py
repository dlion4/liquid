import contextlib
import logging
import os
from datetime import timedelta
from typing import Any

import resend
from celery import shared_task
from django.contrib.auth.models import User as UserObject
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags

from config.settings.base import resend



@shared_task()
def get_users_count():
    """A pointless Celery task to demonstrate usage."""
    return UserObject.objects.count()



logger = logging.getLogger(__name__)

@shared_task
def send_background_email(
    sender: UserObject | None = None,
    template_name: str = "",
    context: dict[str, Any] | None = None,
    recipients: list[str] | list | None = None,
    ):
        """
        A Celery task that sends emails.

        This function is a Celery task that is used to send emails. It does not take any
        parameters and does not return anything.

        This function is decorated with `@shared_task()`, which means it can be executed
        asynchronously by Celery.

        Note: This function currently does not perform any email sending logic and simply
        returns without doing anything.

        """
        if recipients is None:
            recipients = []
        if context is None:
            context = {}
        if context is not None:
            context.update({
                "team": "Earnkraft",
            })

        try:
            html_message = render_to_string(template_name, context)
            subject = context.get("subject", "[Earnkraft Investment] Successful onboarding")
            to = recipients or [context.get("email")]

            params: resend.Emails.SendParams = {
                "from": sender if sender else "Earnkraft <email@earnkraft.com>",
                "to": to,
                "subject": subject,
                "html": html_message,
            }
            email = resend.Emails.send(params)
            logger.info(f"Email successfully sent via Resend API to {to}")
        except Exception as e:
            logger.exception(str(e))




