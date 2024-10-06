from .forms import AccountDepositModelForm
from django.http import HttpRequest

from django.contrib.auth.models import AnonymousUser

def deposit_form_action(request: HttpRequest):
    if isinstance(request.user, AnonymousUser):
        deposit_money_form = None  # Or return an empty form or redirect based on your use case
    else:
        deposit_money_form = AccountDepositModelForm(request=request)
    
    return {'deposit_money_form': deposit_money_form}