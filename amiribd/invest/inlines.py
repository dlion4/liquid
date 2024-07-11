from .models import PoolFeature, Account, Plan, SavingInvestmentPlan
from amiribd.transactions.models import Transaction
from nested_inline.admin import NestedStackedInline
from .forms import AdminAddPlanForm,AdminAccountForm,AdminTransactionForm
from unfold import admin as unfold_admin
class TransactionInline(unfold_admin.StackedInline, NestedStackedInline):
    model = Transaction
    extra = 1
    fk_name = "account"
    form = AdminTransactionForm
    readonly_fields = ["receipt_number"]


class PlanInline(unfold_admin.StackedInline, NestedStackedInline):
    model = Plan
    extra = 1
    form = AdminAddPlanForm
    fk_name = "account"


class AccountInline(unfold_admin.StackedInline,NestedStackedInline):
    model = Account
    extra = 1
    # form = AdminAccountForm
    fk_name = "pool"
    inlines = [TransactionInline, PlanInline]


class PoolFeatureInline(unfold_admin.StackedInline,NestedStackedInline):
    model = PoolFeature
    extra = 0
    fk_name = "pool"

class SavingInvestmentPlanInline(unfold_admin.StackedInline, NestedStackedInline):
    model = SavingInvestmentPlan
    extra = 0
    fk_name = "scheme"