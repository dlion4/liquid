import json
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.


def mpesa_callback_url(request):
    payload: str | bytearray | bytes = request.body or "request body data"

    return JsonResponse(
        {
            "message": "Mpesa callback url",
            "status": 200,
            "data": {"url": "https://mpesa.com", "payload": json.loads(payload)},
        }
    )
