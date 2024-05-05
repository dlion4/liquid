from django.http import HttpResponsePermanentRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class AccountStatusMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path.startswith("/dashboard/"):

            if not request.user.is_authenticated:
                return HttpResponsePermanentRedirect(reverse("users:login"))

            print("Middleware running inside dashboard")
            account = request.user
            # Redirect based on account status
            print(account.status)
            target_path = None
            if account.status == "COMPLETED":
                if account.verified:
                    target_path = reverse("dashboard:home")
                else:
                    target_path = reverse("dashboard:welcome")
            elif account.status == "PENDING":
                target_path = reverse("dashboard:welcome")
            elif account.status == "BLOCKED":
                target_path = reverse("dashboard:blocked")
            elif account.status == "SUSPENDED":
                target_path = reverse("dashboard:suspended")

            # Check if the current path is already the target path to prevent redirect loops
            if target_path and request.path != target_path:
                return HttpResponsePermanentRedirect(target_path)
        return response
