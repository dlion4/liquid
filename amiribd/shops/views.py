import json
from django.http import HttpRequest, HttpResponseRedirect
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from .forms import ShopItemForm, ShopItemOfferForm
from .models import ShopItem
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, CreateView
# Create your views here.
from typing import Any
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class ShopItemCreateView(LoginRequiredMixin, FormView):
    form_class = ShopItemForm
    def get_success_url(self) -> str:
        return HttpResponseRedirect(redirect_to=self.request.META.get("HTTP_REFERER"))
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.profile = self.request.user.profile_user
        instance.save()
        form.save()
        return self.get_success_url()
    


class ShopItemOfferView(View):
    form_class = ShopItemOfferForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)
    

    def get_shop_item(self, item_id):
        item = get_object_or_404(ShopItem, pk=int(item_id))
        return item
    
    def post(self, request, *args, **kwargs):
        item_id = kwargs.pop('item_id', None)
        data = json.loads(request.body)
        form = self.form_class(data=data)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.client = self.request.user.profile_user
            instance.shop_item = self.get_shop_item(item_id)
            instance.save()
            form.save(commit=True)
            return JsonResponse({"success":True,"msg":"Offer sent to the seller successfully"})
        return JsonResponse({"success":False, "msg":json.dumps(form.errors)})
