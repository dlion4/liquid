from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.

def mpesa_callback_url(request):
    return JsonResponse({"message":"Mpesa callback url"})

