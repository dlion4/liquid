from django.urls import reverse
from django.shortcuts import get_object_or_404
from amiribd.users.actions import generate_referral_code
from django.http import JsonResponse, HttpResponse

from amiribd.users.models import User, Profile
import time
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def generate_referral(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    time.sleep(5)
    referral_code = generate_referral_code(profile.user.pk)
    profile.referral_code = referral_code
    profile.save()
    return HttpResponse(referral_code)
