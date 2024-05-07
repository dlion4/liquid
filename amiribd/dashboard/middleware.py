from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


class AccountStatusMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/dashboard/"):
            return self.handle_dashboard_request(request)
        return self.get_response(request)

    def handle_dashboard_request(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("users:login"))

        account = request.user
        target_path = self.get_redirect_path(request, account)

        if (
            target_path
            and request.path != target_path
            and target_path not in ["/dashboard/kyc/", "/dashboard/invest/"]
        ):
            return HttpResponseRedirect(target_path)

        return self.get_response(request)

    def get_redirect_path(self, request, account):
        try:
            if account.status == "COMPLETED":
                return (
                    request.path if account.verified else reverse("dashboard:welcome")
                )
            elif account.status == "PENDING":
                return reverse("dashboard:welcome")
            elif account.status == "BLOCKED":
                return reverse("dashboard:blocked")
            elif account.status == "SUSPENDED":
                return reverse("dashboard:suspended")
        except AttributeError as e:
            logger.error(f"Error accessing user account properties: {e}")
        return None
