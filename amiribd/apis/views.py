import json
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.


def mpesa_callback_url(request):

    print(request.body)
    print(request.headers)
    print(request.method)

    return JsonResponse(
        {
            "message": "Mpesa callback url",
            "status": 200,
            "data": {"url": "https://mpesa.com", "payload": "some data"},
        }
    )
