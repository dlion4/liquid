from typing import TYPE_CHECKING

from django.http import JsonResponse

if TYPE_CHECKING:
    from amiribd.users.models import Profile as ProfileModel


def validate_profile_plan_purchase_status(request) -> JsonResponse:
    try:
        profile: ProfileModel = request.user.profile_user
        has_unpaid_plan = profile.plans.filter(is_paid=False).exists()
        profile_level = profile.subscription_level
        return JsonResponse(
            {
                "success": True,
                "has_unpaid_plan": has_unpaid_plan,
                "profile_level": profile_level,
            },
            status=200,
        )
    except (profile.DoesNotExist, Exception) as e:
        return JsonResponse(
            {"success": False, "error": str(e)}, status=400,
        )
