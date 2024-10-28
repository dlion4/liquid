import random
import string

from django.conf import settings


def generate_referral_code(user_pk):
    random_str = "".join(random.choices(string.ascii_letters + string.digits, k=45))  # noqa: S311
    return f"LQ-{user_pk}-{random_str}"


def build_signup_referral_link(request, profile):
    return f"{settings.EARNKRAFT_AUTH_SERVICE_URL}/register/{profile.referral_code}"

# http://localhost:5173/register/yy-11-fz0sz2oj1q5a8b7ra8o8v2phg67r5n9oyie8yt11m0qg4-1730107669
