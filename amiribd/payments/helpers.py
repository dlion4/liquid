from django.http import JsonResponse
from django.urls import reverse
from django.views import View
from intasend import APIService
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site


class MpesaStkPushSetUp:
    # publishable_key = settings.INTASEND_PUBLISHABLE_KEY
    # secret_key = settings.INTASEND_SECRET_KEY
    publishable_key =''
    secret_key = ''

    def mpesa_stk_push_service(self):

        return APIService(
            token=self.secret_key,
            publishable_key=self.publishable_key,
            test=settings.INTASEND_TEST_MODE,
        )

def generate_paystack_webhook_url(request, *args, **kwargs):
    # Generate the relative URL
    relative_url = reverse("payments:paystack:paystack-webhook-callback")
    
    # Build the absolute URL
    absolute_url = request.build_absolute_uri(reverse("payments:paystack:paystack-webhook-callback"))
    
    # Return or use the absolute URL as needed
    return JsonResponse({'webhook_url': absolute_url})

    
    