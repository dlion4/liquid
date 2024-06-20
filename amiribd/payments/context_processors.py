from django.urls import reverse


def payment_context_data(request):
    webhook_url =request.build_absolute_uri(reverse("payments:paystack:paystack-webhook-callback"))
    payment_webhook_status_url = reverse("payments:paystack:paystack-webhook-status")
    return dict(
        webhook_url = webhook_url,
        payment_webhook_status_url = payment_webhook_status_url,
    )