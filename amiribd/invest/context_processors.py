from amiribd.invest.forms import AccountEventWithdrawalForm


def withdrawal_form_action(request):
    withdrawal_form = AccountEventWithdrawalForm()
    return {"withdrawal_form": withdrawal_form}
