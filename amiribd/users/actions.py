import random
import string

from django.urls import reverse


def generate_referral_code(user_pk):
    random_str = "".join(random.choices(string.ascii_letters + string.digits, k=45))  # noqa: S311
    return f"LQ-{user_pk}-{random_str}"


def build_signup_referral_link(request, profile):
    return request.build_absolute_uri(
        reverse(
            "users:referred-signup",
            kwargs={"referral_code": profile.referral_code},
        ),
    )
