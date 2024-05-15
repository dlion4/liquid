from amiribd.invest.forms import (
    AccountEventWithdrawalForm,
    AddPlanForm,)

def display_add_plan_form(request):
    return {
            "add_plan_form": AddPlanForm(request=request)
        }