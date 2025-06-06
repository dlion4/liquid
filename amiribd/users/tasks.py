import logging
from typing import Any
import resend
import requests
from celery import shared_task
from django.contrib.auth.models import User as UserObject
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from config.settings.base import env

RESEND_API_KEY = env.str("RESEND_EMAIL_SERVICE_API_KEY", "")


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

        # message = EmailMultiAlternatives(  # noqa: ERA001, RUF100
        #     subject, body=strip_tags(html_message), from_email=from_email, to=to)
        # message.attach_alternative(html_message, mimetype="text/html")  # noqa: ERA001
        # message.send()  # noqa: ERA001

        response = send_email_with_attachment(
            
            "Earnkraft <Admin@earnkraft.com>",
            to,
            subject,
            html_message,
        )
        
        if response.get("id", None): 
            logger.info(f"Email sent successfully to {to}")  # noqa: G004
        else:
            logger.error(f"Failed to send email to {to}. Error: {response.text}")  # noqa: G004
    except Exception as e:
        logger.exception(str(e))  # noqa: TRY401


def send_email_with_attachment(
    
    default_from_email:str="",
    to:list[str]=[""],
    subject:str="", html_content: str=""):

    params: resend.Emails.SendParams = {
        "from": default_from_email ,
        "to": to,
        "subject": subject,
        "html": html_content,
    }

    resend.api_key = RESEND_API_KEY
    response=resend.Emails.send(params)
    return response
    
    
