import logging
from typing import Any
import contextlib
from celery import shared_task
from django.contrib.auth.models import User as UserObject
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from datetime import timedelta


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
            plain_message = strip_tags(html_message)
            subject = context.get("subject", "[Earnkraft Investment] Successful onboarding")
            from_email = context.get("from_email", sender.email if sender else None)
            to = recipients or [context.get("email")]

            logger.info(f'Sending email from {from_email} to {to} with subject "{subject}"')  # noqa: E501, G004

            message = EmailMultiAlternatives(
                subject=subject,
                body=plain_message,
                from_email=from_email,
                to=to,
            )

            message.attach_alternative(html_message, "text/html")
            message.send()

            logger.info(f"Email successfully sent to {to}")  # noqa: G004
        except Exception as e:
            logger.exception(e)




