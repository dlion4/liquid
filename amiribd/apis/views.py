import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from amiribd.rates.serializers import KenyaConversionModelSerializer
from amiribd.rates.models import KenyaConversion
from rest_framework import generics
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

class LoadCurrencyConversionRatesView(generics.ListAPIView):
    serializer_class = KenyaConversionModelSerializer
    queryset = KenyaConversion.objects.all()
