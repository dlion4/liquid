from amiribd.invest.forms import (
    AccountEventWithdrawalForm,
    AddPlanForm,
)


def display_add_plan_form(request):
    if request.user.is_authenticated:
        return {"add_plan_form": AddPlanForm(request=request)}
    return {"add_plan_form": AddPlanForm()}
