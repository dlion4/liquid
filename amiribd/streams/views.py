from itertools import groupby
import json
from typing import Any
from django import http
from django.http import  (
    HttpRequest, 
    HttpResponse, 
    JsonResponse,
    StreamingHttpResponse    
)
from django.views.decorators.http import require_GET
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import TemplateView
from amiribd.dashboard.views import SupportView
from amiribd.streams.models import Room
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from amiribd.users.models import Profile
from amiribd.streams.serializers import MessageSerializer
from .models import Inbox, Message
from django.utils.timezone import localdate, localtime
from amiribd import redis_client
# Create your views here.


class RoomView(SupportView):
    template_name = "account/dashboard/v1/rooms/room.html"
    model = Room

    def get_object(self):
        return get_object_or_404(self.model, slug=self.kwargs.get("room_slug"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["room"] = self.get_object()
        return context


class MessageInboxRetrieveCreateView(View):
    # template_name = "account/dashboard/v1/rooms/private/message_inbox.html"
    # @method_decorator(csrf_exempt)
    # def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
    #     return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        # create a message object
        message, _ = Message.objects.get_or_create(
            sender=Profile.objects.get(pk=data.get("profile_pk")),
            receiver=Profile.objects.get(pk=data.get("network_pk")),
        )
        serializer = MessageSerializer(message).data
        print("data", data)
        return JsonResponse({"success": True, "message": serializer})


# This decorator restricts this view to only handle POST requests
def create_retrieve_message(request):
    # Your logic here

    return JsonResponse({"success": True})


class MessageInboxView(SupportView):
    template_name = "account/dashboard/v1/rooms/private/message_inbox.html"

    def __get_message(self, **kwargs):
        return get_object_or_404(
            Message,
            pk=kwargs.get("pk"),
            receiver__user__username__iexact=kwargs.get("receiver").lstrip("@"),
            sender=self.request.user.profile_user,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message"] = self.__get_message(**kwargs)
        context["inbox_messages"] = self.__inbox_private__messages(**kwargs)
        return context

    def __inbox_private__messages(self, **kwargs):
        inbox_messages = Inbox.objects.filter(
            message=self.__get_message(**kwargs)
        ).order_by("-created_at")

        return {
            date: list(items)
            for date, items in groupby(
                inbox_messages, key=lambda item: localtime(item.created_at).date()
            )
        }
