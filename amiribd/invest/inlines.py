from nested_inline.admin import NestedStackedInline
from unfold import admin as unfold_admin

from amiribd.transactions.models import Transaction

from .forms import AdminAddPlanForm
from .forms import AdminTransactionForm
from .models import Account
from .models import Plan
from .models import PoolFeature
from .models import SavingInvestmentPlan


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
