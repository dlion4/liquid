
from django.http import JsonResponse
from rest_framework import generics

from amiribd.rates.models import KenyaConversion
from amiribd.rates.serializers import KenyaConversionModelSerializer

# Create your views here.


def mpesa_callback_url(request):

    return JsonResponse(
        {
            "message": "Mpesa callback url",
            "status": 200,
            "data": {"url": "https://mpesa.com", "payload": "some data"},
        },
    )

class LoadCurrencyConversionRatesView(generics.ListAPIView):
    serializer_class = KenyaConversionModelSerializer
    queryset = KenyaConversion.objects.all()
