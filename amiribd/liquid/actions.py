from django.core.mail import send_mail
import after_response


@after_response.enable
def send_email_after_response(to, subject, body):
    send_mail(subject, body, "me@example.com", [to])
