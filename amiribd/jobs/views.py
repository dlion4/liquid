import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from amiribd.jobs.models import Job
from amiribd.users.models import Profile
from .forms import JobApplicationForm
from django.core.exceptions import PermissionDenied
from django.db import transaction
from amiribd.users.views import send_welcome_email
# Create your views here.

@login_required
@require_POST
@transaction.atomic
def job_application_view(request, job_id, applicant_id):
    try:
        # Example: Saving form data to database
        with transaction.atomic():
            url = request.POST.pop("path")
            form = JobApplicationForm(
                request.POST, request.FILES, job_id=job_id, applicant_id=applicant_id)
            if form.is_valid():
                form.save(commit=True)
                return JsonResponse(
                    {"message":"Application sent successfully", 
                     "success": True,
                     "url": url,
                     })
            return JsonResponse({"message":json.dumps(form.errors), "success": False})
    except Exception as e:
        return JsonResponse({"message": str(e), "success": False})


def send_application_nofication_email_to_applicant(channel, user, template_name, context:dict={}):
    if "@" in channel:
        send_welcome_email.after_response(user, template_name, context=context)
    else:
        pass
