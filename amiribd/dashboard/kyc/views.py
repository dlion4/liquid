from typing import Any
from django.views.generic import TemplateView
from amiribd.dashboard.guard import DashboardGuard
from amiribd.users.models import Profile, Address, Document
from amiribd.users.forms import (
    ProfileAddressForm,
    ProfileVerificationDocumentForm,
    ProfileDetailForm,
)
import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from django.urls import reverse, reverse_lazy
from django import forms
from django.views.generic.edit import FormView


class ProfileUpdateKycView(DashboardGuard, TemplateView):
    template_name = "account/dashboard/components/forms/kyc/detail.html"
    form_class = ProfileDetailForm
    success_url = reverse_lazy("kyc:address")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class(user=self._get_user())
        return context

    # def form_valid(self, form):
    #     # process later
    #     return redirect(self.success_url)

    def post(self, request, **kwargs):
        form = self.form_class(request.POST, user=self._get_user())
        if form.is_valid():
            # form.save()
            return redirect(self.success_url)
        print(form.errors)
        return render(request, self.template_name, {"form": form})


kyc_profile_detail = ProfileUpdateKycView.as_view()


class ProfilUpdateAddressKycView(DashboardGuard, TemplateView):
    template_name = "account/dashboard/components/forms/kyc/address.html"
    form_class = ProfileAddressForm
    success_url = reverse_lazy("kyc:document")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        return context

    def post(self, request, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # form.save()
            return redirect(self.success_url)
        print(form.errors)
        return render(request, self.template_name, {"form": form})


kyc_profile_address = ProfilUpdateAddressKycView.as_view()


class ProfileUpdateIdentityKycView(DashboardGuard, FormView):
    template_name = "account/dashboard/components/forms/kyc/documents.html"
    form_class = ProfileVerificationDocumentForm
    success_url = reverse_lazy("dashboard:home")

    def form_valid(self, form):
        # process later
        return super().form_valid(form)


kyc_profile_identify = ProfileUpdateIdentityKycView.as_view()
