import json
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from amiribd.users.models import User, Profile
from amiribd.users.views import HtmxSetupView
from django.views.generic import View


class ValidateUniquePhoneNumberView(HtmxSetupView):

    def get(self, request, *args, **kwargs):
        if phone_number := request.GET.get("phone_number"):
            print(phone_number)
            if Profile.objects.filter(phone_number=phone_number).exists():
                return HttpResponse(self.fail_html_response())
        return HttpResponse(self.success_html_response())

    def fail_html_response(self, *args, **kwargs):
        self.html_swap_message = """
            <small class='text-muted uk-text-danger' data-bt-state='disabled' id='phone-number-error-message'>Phone number already taken</small>
        """

        return self.html_swap_message

    def success_html_response(self, *args, **kwargs):
        self.html_swap_message = """
                <small class='text-muted uk-text-success' id='phone-number-error-message'></small>
            """

        return self.html_swap_message


class ValidatedObValidView(HtmxSetupView):
    def get(self, request, *args, **kwargs):
        print(request.GET.get("date_of_birth"))

        return HttpResponse("self.success_html_response()")
