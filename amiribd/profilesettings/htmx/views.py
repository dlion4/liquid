from typing import Any
from django.views import View
from django.db import transaction
from amiribd.htmx.account.views import HtmxDispatchView
from django.http import JsonResponse
import contextlib
from amiribd.users.models import Profile
from amiribd.profilesettings.models import NotificationSubscription, NotificationType


def htmx_notifications_form(request):
    pass


class HandleNotificationSwitcherView(HtmxDispatchView):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        notification_type_id = kwargs.get("notification_type")
        profile_id = kwargs.get("profile")

        notification_type = NotificationType.objects.get(id=notification_type_id)

        # with contextlib.suppress(Exception):

        notification_type = NotificationType.objects.get(id=notification_type_id)
        profile = Profile.objects.get(id=profile_id)
        notification_type.profile.add(profile)

        # with contextlib.suppress(Exception):
        subscription, _ = NotificationSubscription.objects.get_or_create(
            notify_label_type=notification_type, profile=profile
        )
        subscription.is_active = True
        subscription.save()

        return JsonResponse(
            {"success": True, "message": "Subscription successfully added"}
        )

        # return JsonResponse({"success": False, "message": "Subscription failed"})

    def get(self, request, *args, **kwargs):

        notification_type_id = kwargs.get("notification_type")
        profile_id = kwargs.get("profile")

        notification_type = NotificationType.objects.get(id=notification_type_id)

        # with contextlib.suppress(Exception):

        notification_type = NotificationType.objects.get(id=notification_type_id)
        profile = Profile.objects.get(id=profile_id)
        notification_type.profile.remove(profile)

        # with contextlib.suppress(NotificationSubscription.DoesNotExist):
        subscription = NotificationSubscription.objects.get(
            notify_label_type=notification_type, profile=profile, is_active=True
        )
        subscription.is_active = False
        subscription.save()

        return JsonResponse(
            {"success": True, "message": "Subscription successfully removed"}
        )


class ProfileNotificationSubscribeLookupView(View):
    # htmx_template_name = "account/profile/partials/notifications.html"

    def get(self, request, *args, **kwargs):
        notification_type_id = request.GET.get("notification_type_id")
        profile_id = request.GET.get("profile_id")

        notification_type = NotificationType.objects.get(id=notification_type_id)
        profile = Profile.objects.get(id=profile_id)

        subscribed = NotificationSubscription.objects.filter(
            notify_label_type=notification_type, profile=profile, is_active=True
        )

        if subscribed.exists():
            for sub in subscribed:
                ntype = sub.notify_label_type.pk
                return JsonResponse({"success": True, "subscribed": ntype})
        return JsonResponse(
            {
                "success": False,
            }
        )
