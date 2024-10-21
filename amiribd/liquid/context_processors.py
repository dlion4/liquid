from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest
from django.urls import reverse

from amiribd.users.forms import EmailLoginForm
from amiribd.users.forms import EmailSignupForm
from config.settings.base import env

from .forms import ContactForm
from .models import CompanyTermsAndPolicy


def liquid_site_data(request:HttpRequest):
    return {
        "site_name": "AmiriBD",
        "website_url": request.build_absolute_uri(reverse("home")),
        "profile_dashboard": request.build_absolute_uri(reverse("dashboard:home")),
        "contact_form": ContactForm(),
        "address": "Satrio Tower 16th Floor, Jl. Prof Dr Satrio Kuningan, Jakarta",
        "officephone": "contact Us",
        "officeemail": "support@earnkraft.com",
        "company_privacy_document": CompanyTermsAndPolicy.objects.first(),
        "external_links": {
            "blogging_site": {"domain": "earnkraft.com", "url": "https://earnkraft.com"},
        },
        "login_form": EmailLoginForm(),
        "register_form": EmailSignupForm(),
        "paystack_live_key": env.str("PAYSTACK_LIVE_API_KEY", ""),
        "paystack_test_key": env.str("PAYSTACK_TEST_API_KEY", ""),
        "ZERO_BOUNCE_PROJECT_TOKEN": "DaeIKDQhKLxDkpjHLW9QtoonLPFnL53CijFAiH8MSMiCb6G0CWV14PxSbRdbn9MvkXV9N7vh8if8kpdDahQSS8wI1k1tMiv5z9bnXkarrDrbwSQZaP7PS8KsUC7egHZTiDDY9XBcsGfnc1Jn0O0kF0e5Aa9wL2flyh0APX7sPs8fAwukl4wlUCIEEzzL0VkKMuPTnqpm1uF17bTi18UPsm6enWlqIOJzJ5P1ftdOmJEqDZBXh1qy2oFO23S74nS",
    }
