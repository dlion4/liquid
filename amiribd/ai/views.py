import json

from django.db import transaction
from django.http import JsonResponse
from django.views import View
from g4f.client import Client

client = Client()


class AIGenerateContentView(View):

    async def get(self, request, *args, **kwargs):
        return JsonResponse({"message": "success", "success": True})

    @transaction.non_atomic_requests
    async def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        content = data.get("content")
        return JsonResponse({"success": True, "response": json.dumps(content)})
