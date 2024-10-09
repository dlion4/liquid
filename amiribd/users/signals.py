
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import IntegrityError
import contextlib
from .models import User, ValidatedEmailAddress
import threading


@receiver(post_save, sender=User)
def create_validated_email_on_signup(sender, instance, created, **kwargs):
    if created:
        threading.Thread(target=create_validated_email_address, args=(instance.email)).start()

def create_validated_email_address(user: User, email_address:str)->None:
    """
    Validates an email address.
    """
    # Add your email validation logic here
    # ...
    with contextlib.suppress(IntegrityError):
        ValidatedEmailAddress.objects.using("email_validation").create(email_address=email_address)
