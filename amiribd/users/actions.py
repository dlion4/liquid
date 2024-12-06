import random
import string

from django.http import HttpRequest
from django.urls import reverse


def generate_referral_code(user_pk):
    random_str = "".join(
        random.choices(string.ascii_letters + string.digits, k=45),  # noqa: S311
    )
    return f"LQ-{user_pk}-{random_str}"


def build_signup_referral_link(request: HttpRequest, profile):
    full_domain_name = f"{request.scheme}://{request.get_host()}"
    reverse_path = reverse(
        "users:referred-signup",
        kwargs={"referral_code": profile.referral_code},
    )
    return f"{full_domain_name}{reverse_path}"
