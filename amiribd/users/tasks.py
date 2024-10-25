import logging
from typing import Any
import requests
from celery import shared_task
from django.contrib.auth.models import User as UserObject
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from config.settings.base import env

MAIL_GUN_API_KEY = env.str("MAIL_GUN_API_KEY", "")


@shared_task()
def get_users_count():
    """A pointless Celery task to demonstrate usage."""
    return UserObject.objects.count()


logger = logging.getLogger(__name__)

EXPECTED_MAILGUN_STATUS_CODE = 200

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
        context.update({"team": "Earnkraft"})

    try:
        html_message = render_to_string(template_name, context)
        from_email = settings.DEFAULT_FROM_EMAIL
        subject = context.get("subject", "[Earnkraft Investment] Successful onboarding")
        to = recipients or [context.get("email")]

        logger.info(f'Sending email from {from_email} to {to} with subject "{subject}"')  # noqa: G004

        message = EmailMultiAlternatives(
            subject, body=strip_tags(html_message), from_email=from_email, to=to)
        message.attach_alternative(html_message, mimetype="text/html")
        message.send()
        # response = send_email_with_attachment(
        #     MAIL_GUN_API_KEY,
        #     "Earnkraft <no-reply@earnkraft.com>",
        #     to,
        #     subject,
        #     html_message,
        # )
        # response.raise_for_status()
        # if response.status_code == EXPECTED_MAILGUN_STATUS_CODE:
        logger.info(f"Email sent successfully to {to}")  # noqa: E501, G004
        # else:
        #     logger.error(f"Failed to send email to {to}. Error: {response.text}")  # noqa: E501, G004
    except Exception as e:
        logger.exception(str(e))


def send_email_with_attachment(
    mailgun_api_key:str,
    default_from_email:str,
    to:list[str],
    subject:str, html_content: str):
    response = requests.post(
        "https://api.mailgun.net/v3/earnkraft.com/messages",
        auth=("api", mailgun_api_key),
        data={
            "from": default_from_email,
            "to": to,
            "subject": subject,
            "html": html_content,
        },
        timeout=50,
    )
    response.raise_for_status()
    return response
