
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from amiribd.users.models import Profile
from amiribd.users.utils import generate_referral_code


@csrf_exempt
def generate_referral(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    referral_code = generate_referral_code(profile.user.pk)
    profile.referral_code = referral_code
    profile.save()
    return HttpResponse(referral_code)
