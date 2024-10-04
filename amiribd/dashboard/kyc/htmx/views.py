
from django.http import HttpResponse

from amiribd.users.models import Profile
from amiribd.users.views import HtmxSetupView


class ValidateUniquePhoneNumberView(HtmxSetupView):

    def get(self, request, *args, **kwargs):
        if phone_number := request.GET.get("phone_number"):
            if Profile.objects.filter(phone_number=phone_number).exists():
                return HttpResponse(self.fail_html_response())
        return HttpResponse(self.success_html_response())

    def fail_html_response(self, *args, **kwargs):
        self.html_swap_message = """
            <small
            class='text-muted uk-text-danger' data-bt-state='disabled'
            id='phone-number-error-message'>Phone number already taken</small>
        """
        return self.html_swap_message

    def success_html_response(self, *args, **kwargs):
        self.html_swap_message = """
                <small class='text-muted uk-text-success'
                id='phone-number-error-message'></small>
            """
        return self.html_swap_message


class ValidatedObValidView(HtmxSetupView):
    def get(self, request, *args, **kwargs):
        return HttpResponse("self.success_html_response()")
