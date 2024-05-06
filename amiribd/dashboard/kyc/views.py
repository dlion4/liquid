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
from django.http import HttpResponse, HttpResponseRedirect

from django.urls import reverse, reverse_lazy
from django import forms, http
from django.views.generic.edit import FormView
from django.utils import timezone


class ProfileUpdateKycView(DashboardGuard, TemplateView):
    template_name = "account/dashboard/components/forms/kyc/detail.html"
    form_class = ProfileDetailForm
    success_url = reverse_lazy("kyc:address")

    # doc a guard to check if the user has full name then immediately redirect to the next page

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if self._get_user().profile_user.full_name:
            return redirect(self.success_url)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class(
            initial={
                "email_address": self._get_user().email,
                "public_username": self._get_user().username or "",
            },
        )
        return context

    def post(self, request, **kwargs):
        form = self.form_class(
            request.POST,
            initial={
                "email_address": self._get_user().email,
                "public_username": self._get_user().username or "",
            },
        )
        return self.form_valid(form) if form.is_valid() else self.form_invalid(form)

    def form_valid(self, form):
        profile = Profile.objects.get_or_create(user=self.request.user)[0]
        profile.user.username = form.cleaned_data.get("public_username")
        profile.user.save()

        profile.first_name = form.cleaned_data.get("first_name")
        profile.last_name = form.cleaned_data.get("last_name")
        profile.phone_number = form.cleaned_data.get("phone_number")
        profile.date_of_birth = form.cleaned_data.get("date_of_birth")

        profile.save()

        return redirect(self.success_url)

    def form_invalid(self, form):
        return render(self.request, self.template_name, {"form": form})


kyc_profile_detail = ProfileUpdateKycView.as_view()


class ProfilUpdateAddressKycView(DashboardGuard, TemplateView):
    template_name = "account/dashboard/components/forms/kyc/address.html"
    form_class = ProfileAddressForm
    success_url = reverse_lazy("kyc:document")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        return context

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        profile = Profile.objects.get(user=self._get_user())
        return redirect(self.success_url) if profile.is_address_set else response

    def post(self, request, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return self._save_address_and_set_flag(form)
        print(form.errors)
        return render(request, self.template_name, {"form": form})

    #
    def _save_address_and_set_flag(self, form):
        instance = form.save(commit=False)
        instance.profile = self._get_user().profile_user
        instance.profile.is_address_set = True
        instance.profile.save()
        instance.save()
        form.save()
        return redirect(self.success_url)


kyc_profile_address = ProfilUpdateAddressKycView.as_view()


class ProfileUpdateIdentityKycView(DashboardGuard, FormView):
    template_name = "account/dashboard/components/forms/kyc/documents.html"
    form_class = ProfileVerificationDocumentForm
    success_url = reverse_lazy("kyc:complete_verification")
    samepage_url = ""

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        profile = Profile.objects.get(user=self._get_user())
        return redirect(self.success_url) if profile.is_document_set else response

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.profile = self._get_user().profile_user
        instance.profile.is_document_set = True
        instance.profile.save()
        instance.save()
        print(form.errors)

        return HttpResponseRedirect(
            self.request.META.get("HTTP_REFERER", reverse_lazy("dashboard"))
        )


kyc_profile_identify = ProfileUpdateIdentityKycView.as_view()


class ProfileCompleteKycView(DashboardGuard, TemplateView):
    template_name = "account/dashboard/components/forms/kyc/complete.html"
    success_url = reverse_lazy("dashboard:home")

    def post(self, *args, **kwargs):
        profile = self._get_user().profile_user

        # update the kyc stuff

        profile.kyc_completed = True
        profile.kyc_completed_at = timezone.now()
        profile.user.status = "COMPLETED"
        profile.user.verified = True
        profile.user.save()
        profile.save()

        return redirect(self.success_url)


kyc_profile_complete = ProfileCompleteKycView.as_view()
