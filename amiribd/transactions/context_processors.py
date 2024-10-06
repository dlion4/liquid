from .forms import AccountDepositModelForm
from django.http import HttpRequest

def deposit_form_action(request: HttpRequest):
    deposit_money_form=AccountDepositModelForm(request=request)
    return {"deposit_money_form": deposit_money_form}