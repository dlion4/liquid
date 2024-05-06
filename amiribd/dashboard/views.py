from django.shortcuts import render
from django.views.generic import TemplateView
from .guard import DashboardGuard


# Create your views here.
class DashboardViewMixin(TemplateView):
    template_name = ""

    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self._get_user().profile_user
        return context


class DashboardView(DashboardViewMixin):
    template_name = "account/dashboard/home.html"

    def _get_user(self):
        return self.request.user


dashboard = DashboardView.as_view()


class WelcomeView(DashboardGuard, DashboardViewMixin):
    template_name = "account/dashboard/welcome.html"


welcome = WelcomeView.as_view()
