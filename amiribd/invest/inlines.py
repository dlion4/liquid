from .models import PoolFeature, Account, Plan
from amiribd.transactions.models import Transaction
from nested_inline.admin import NestedStackedInline
from .forms import AdminAddPlanForm,AdminAccountForm,AdminTransactionForm

class TransactionInline(NestedStackedInline):
    model = Transaction
    extra = 1
    fk_name = "account"
    form = AdminTransactionForm
    readonly_fields = ["receipt_number"]


class PlanInline(NestedStackedInline):
    model = Plan
    extra = 1
    form = AdminAddPlanForm
    fk_name = "account"


class AccountInline(NestedStackedInline):
    model = Account
    extra = 1
    form = AdminAccountForm
    fk_name = "pool"
    inlines = [TransactionInline, PlanInline]


class PoolFeatureInline(NestedStackedInline):
    model = PoolFeature
    extra = 0
    fk_name = "pool"
