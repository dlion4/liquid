import json
from django.http import JsonResponse
from django.views import View
from g4f.client import Client
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db import transaction
import asyncio
from concurrent.futures import ThreadPoolExecutor
import time


client = Client()


class AIGenerateContentView(View):

    async def get(self, request, *args, **kwargs):
        return JsonResponse({"message": "success", "success": True})

    @transaction.non_atomic_requests
    async def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        content = data.get("content")

        return JsonResponse({"success": True})
