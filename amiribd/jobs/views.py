from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect
from django.urls import  reverse_lazy
from django.views.decorators.http import require_POST

from amiribd.users.views import send_welcome_email

from .forms import JobApplicationForm

# Create your views here.

@login_required
@require_POST
@transaction.atomic
def job_application_view(request, job_id, applicant_id):
    page_url = reverse_lazy("dashboard:invest:jobs:jobs")
    try:
        form = JobApplicationForm(
            request.POST, request.FILES, job_id=job_id, applicant_id=applicant_id)
        if form.is_valid():
            form.save(commit=True)
            messages.success(
                request,
                "Application submitted successfully. We'll communicate with you in a few"
            )
            return redirect(page_url)
        messages.error(
            request,
            "Could not process application. Kindly check your application request")
        return redirect(page_url)
    except Exception as e:
        messages.warning(
            request, "Oops! Something went wrong with your application")
        return redirect(page_url)

def send_application_nofication_email_to_applicant(channel, user, template_name, context:dict={}):
    if "@" in channel:
        send_welcome_email.after_response(user, template_name, context=context)
    else:
        pass
