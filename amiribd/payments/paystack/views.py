from typing import Any
from django.http import HttpRequest, JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from amiribd.payments.models import PaystackPaymentStatus
from amiribd.payments.serializers import PaystackPaymentStatusSerializer
import requests

class PayStackPaymentCallbackView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        # data = json.loads(request.body)
        # paystack_reference_data = data.get('data')
        # reference = paystack_reference_data.get('reference')
        # status
        """
        1: success
        2: failed
        3: pending
        4: timeout
        """
        # payment_status = PaystackPaymentStatus.objects.create(
        #     email=paystack_reference_data.get('customer').get('email'),
        #     status=paystack_reference_data.get('status'),
        #     reference=reference,
        #     amount=paystack_reference_data.get('amount')/100
        # )

        return JsonResponse({
            "reference": "reference",
            "status":"paystack_reference_data.get('status')",	
        })



class PayStackPaymentStatusView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        # payment_status_object = get_object_or_404(PaystackPaymentStatus, reference=request.GET.get("reference"))
        # serialized_data = PaystackPaymentStatusSerializer(payment_status_object).data
        # reference=request.GET.get("reference")
        
        
        
        return JsonResponse({'data':'data', 'success': True}, safe=False)
