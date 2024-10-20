from django.views.generic import View

from amiribd.transactions.models import Transaction


class CustomTransactionCreationView(View):
    def create_transaction_method(  # noqa: PLR0913
        self,
        profile,
        account,
        type_="DEPOSIT",
        amount=0.00,
        discount=0.00,
        source="Account Registration",
        payment_phone=None,
        mpesa_transaction_code=None,
        payment_phone_number=None,
        currency="KES",
        country="Kenya",
    ):
        return Transaction.objects.create(
            profile=profile,
            account=account,
            type=type_,
            amount=amount,
            discount=discount,
            source=source,
            payment_phone=payment_phone,
            mpesa_transaction_code=mpesa_transaction_code,
            payment_phone_number=payment_phone_number,
            currency=currency,
            country=country,
        )
