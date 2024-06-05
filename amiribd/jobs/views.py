import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import JobApplicationForm
from django.core.exceptions import PermissionDenied
from django.db import transaction
from amiribd.users.views import send_welcome_email
# Create your views here.

@login_required
@require_POST
@transaction.atomic
def job_application_view(request, job_id, applicant_id):
    if request.method == 'POST':
        try:
            # Example: Saving form data to database
            with transaction.atomic():
                form = JobApplicationForm(request.POST, request.FILES, job_id=job_id, applicant_id=applicant_id)
                if form.is_valid():
                    form.save(commit=True)

                    # TODO: Send email to applicant and admin
                    # TODO: Send SMS to applicant and admin
                    return JsonResponse({"message":"Application sent successfully", "success": True})
                
                return JsonResponse({"message":json.dumps(form.errors), "success": False})
                
        except Exception as e:
            print(e)
            return JsonResponse({"message": str(e), "success": False})
        
    raise PermissionDenied()

    




def send_application_tofication_email_to_applicant(channel, user, template_name, context:dict={}):
    if "@" in channel:
        send_welcome_email.after_response(user, template_name, context=context)