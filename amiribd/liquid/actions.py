from django.core.mail import send_mail
import after_response
import contextlib


@after_response.enable
def send_email_after_response(to, subject, body):
    with contextlib.suppress(Exception):
        send_mail(subject, body, "me@example.com", [to])
