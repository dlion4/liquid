from typing import Any
from django import http
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from amiribd.profiles.admin import PlantformAdmin
from amiribd.profiles.forms import PlantformTypeForm
from amiribd.profiles.models import Plantform, PlantformType, Position
from amiribd.profiles.serializers import PositionSerializer
from amiribd.profiles.models import Agent
import contextlib
from django.db import transaction


class ProfileAgentMixinView(LoginRequiredMixin, View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return JsonResponse({"message": "success", "success": True})


class ProfileRegisterVipLevelView(ProfileAgentMixinView):
    def _get_profile(self):
        return self.request.user.profile_user

    @transaction.atomic
    def post(self, request, *args, **kwargs):

        vip_position_choice_id = kwargs.get("vip_position_choice_id")
        position = Position.objects.get(pk=vip_position_choice_id)

        # chec if user is in one of the available positions
        try:
            profile_is_agent = Agent.objects.filter(
                profile=self._get_profile()
            ).exists()
            if not profile_is_agent:
                # create the agent and add him,/her into the respective group

                Agent.objects.create(profile=self._get_profile(), position=position)

                if group := Group.objects.filter(name=position.name).first():
                    self.request.user.groups.add(group)

                return JsonResponse(
                    {
                        "message": f"You are now an agent with position {position.name.title()}",
                        "success": True,
                    }
                )

            # if agent present but the incoming id is not the same as the registered
            #  delete the agent and then create with a new is position that has been posted
            Agent.objects.filter(profile=self._get_profile()).delete()
            Agent.objects.create(profile=self._get_profile(), position=position)
            # then update the groups if only the group exists
            if group := Group.objects.filter(name=position.name).first():
                self.request.user.groups.add(group)
            return JsonResponse(
                {"message": "You are already an agent", "success": False}
            )

        except Exception as e:
            position_data = PositionSerializer(position).data
            print(position)
            return JsonResponse(
                {
                    "message": "success",
                    "success": False,
                    "position": position_data,
                    "error": str(e),
                }
            )


class ProfileFilterAgentView(ProfileAgentMixinView):
    def _get_profile(self):
        return self.request.user.profile_user

    def get(self, request, *args, **kwargs):
        profile = self._get_profile()
        if agent := Agent.objects.filter(profile=profile).first():
            #  return the position id that the user is assigned
            return JsonResponse({"position": agent.position.pk})
        return JsonResponse({"message": "success", "success": False})
    

class ProfileFilterAgentPlatformView(ProfileAgentMixinView):
    def _get_profile(self):
        return self.request.user.profile_user

    def get(self, request, *args, **kwargs):
        profile = self._get_profile()
        if agent := Agent.objects.filter(profile=profile).first():
            if agent.plantform.exists():
                return JsonResponse({"platforms": [platform.plantform_type.pk for platform in agent.plantform.all()], "success": True})
            return JsonResponse({"message": "success", "success": False})
        return JsonResponse({"message": "success", "success": False})


class ProfileAgentPlantFormSelectionView(ProfileAgentMixinView):
    def _get_profile(self):
        return self.request.user.profile_user


    def delete(self, request, *args, **kwargs):
        return JsonResponse({"message": "success", "success": True})

    def post(self, request, *args, **kwargs):
        platform_type_id = kwargs.get("platform_type_id")
        platform_type = PlantformType.objects.get(pk=platform_type_id)
        # check if such platform type exists for the current user
        agent = Agent.objects.filter(profile=self._get_profile()).first()
        platform = (
            agent.plantform.filter(plantform_type=platform_type).first()
            if agent
            else None
        )

        if not platform and agent:

            plantform = Plantform.objects.create(plantform_type=platform_type)
            agent.plantform.add(plantform)

            print(plantform)
            print(agent)

            return JsonResponse(
                {"message": "success", "success": True, "pk": plantform.pk}
            )

        return JsonResponse(
            {"message": "success", "success": True, "pk": platform_type.pk}
        )

    def get(self, request, *args, **kwargs):
        platform_type_id = request.GET.get("platform_type_id")
        platform_type = PlantformType.objects.get(pk=platform_type_id)
        # check if such platform type exists for the current user
        agent = Agent.objects.filter(profile=self._get_profile()).first()

        platform = (
            agent.plantform.filter(plantform_type=platform_type).first()
            if agent
            else None
        )

        if platform:
            # remove the platform
            platform.delete()
            return JsonResponse({"message": "success", "success": True})
        return JsonResponse({"message": "success", "success": False})
