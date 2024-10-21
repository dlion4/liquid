from mimetypes import guess_type

from django.contrib import messages
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from .actions import send_email_after_response
from .forms import ContactForm
from .models import CompanyTermsAndPolicy
from .models import Contact

# Create your views here.


class HomeView(TemplateView):
    template_name = "home/home.html"



class AboutView(TemplateView):
    template_name = "pages/about.html"


class InvestmentView(TemplateView):
    template_name = "pages/investment.html"


class EducationView(TemplateView):
    template_name = "pages/learn.html"


class EducationView(TemplateView):
    template_name = "pages/learn.html"


class ContactView(FormView):
    template_name = "pages/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        # Process the form data here, e.g., send an email
        # form.save()
        send_email_after_response.after_response(
            form.cleaned_data["email"],
            "New message from website",
            "New message from website",
        )
        messages.success(self.request, "Your message has been sent successfully.")
        return super().form_valid(form)


class HelpView(TemplateView):
    template_name = "pages/help.html"


class GuideView(TemplateView):
    template_name = "pages/guide.html"


class CustomersView(TemplateView):
    template_name = "pages/customers.html"


class CareerView(TemplateView):
    template_name = "pages/career.html"


class PolicyView(TemplateView):
    template_name = "pages/policies.html"






def view_policy(request, pk):
    policy = CompanyTermsAndPolicy.objects.get(pk=pk)
    file_path = policy.file.path
    try:
        with open(file_path, "rb") as f:
            file_content = f.read()
    except FileNotFoundError as e:
        msg = "File does not exist"
        raise Http404(msg) from e

    # Guess the content type of the file
    content_type, encoding = guess_type(file_path)
    if content_type is None:
        content_type = "application/octet-stream"

    # Create the response
    response = HttpResponse(file_content, content_type=content_type)
    response["Content-Disposition"] = "inline; filename=" + policy.file.name

    return response

class CareerApplication(TemplateView):
    template_name = "career/application.html"
