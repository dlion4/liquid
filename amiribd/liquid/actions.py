import contextlib

import after_response
from django.contrib import messages
from django.core.mail import send_mail
from django.utils import timezone

from amiribd.liquid.models import AdminSendMail
from amiribd.liquid.models import AdminSendMailCategory
from amiribd.users.tasks import send_background_email


@after_response.enable
def send_email_after_response(to, subject, body):
    with contextlib.suppress(Exception):
        send_mail(subject, body, "me@example.com", [to])

def send_email_to_user(
    self, request, recipient,
    template="", mail_group=""):
    try:
        email_category = AdminSendMailCategory.objects.get(name__iexact=mail_group)
        email_content = AdminSendMail.objects.get(category=email_category)
        send_background_email(
            sender=None,
            template_name=template,
            context={
                "subject": email_content.subject,
                "message": email_content.message,
                "title": email_content.subject,
            },
            recipients=[recipient.email],
        )
        email_content.sent_at= timezone.now()
        email_content.save()
        self.message_user(
            request,
            f"Email sent to {recipient.email} successfully",
            level=messages.SUCCESS,
        )
    except (AdminSendMailCategory.DoesNotExist, AdminSendMail.DoesNotExist):
        self.message_user(
            request,
            f"""You've not created a message content or
            email category for {mail_group}""",
            level=messages.ERROR,
        )
