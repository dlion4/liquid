from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from .forms import ContactForm
from .models import Contact
from django.urls import reverse_lazy
from django.contrib import messages
from .actions import send_email_after_response

# Create your views here.


class HomeView(TemplateView):
    template_name = "pages/home.html"


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
