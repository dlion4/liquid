from django.shortcuts import render
from django.views.generic import TemplateView
from .guard import DashboardGuard

# Create your views here.


def dashboard(request):
    return render(request, "account/dashboard/home.html")


class WelcomeView(DashboardGuard, TemplateView):
    template_name = "account/dashboard/welcome.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self._get_user().profile_user
        return context


welcome = WelcomeView.as_view()


