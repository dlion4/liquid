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


# class HandlePaymentCreateTransactionView(
#     LoginRequiredMixin, CustomTransactionCreationView
# ):
#     """
#     Handles the creation of payment transactions and updates related accounts and plans,
#     including referral account updates when applicable.
#     """

#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)

#     @transaction.atomic
#     def post(self, request, *args, **kwargs):
#         """
#         Main entry point for handling payment transaction creation.
#         This method organizes
#         the transaction, updates the plan, account, and user profile, and
#         processes referrals if applicable.
#         """
#         profile = request.user.profile_user
#         data = json.loads(request.body)

#         # Step 1: Validate and Retrieve Data
#         phone_number, currency, country = self._retrieve_basic_data(data, profile)

#         # Step 2: Retrieve Objects and Verify Plan Existence
#         pool, account, plan = self._retrieve_transaction_objects(profile, kwargs)
#         if self._is_plan_already_added(profile, plan):
#             pass

#         # Step 3: Calculate Investment Amount and Discount
#         total_investment, discount_price = self._calculate_amounts(
#             data, pool, account, plan,
#         )

#         # Step 4: Create Transaction
#         transaction = self._create_transaction(
#             profile,
#             account,
#             total_investment,
#             discount_price,
#             phone_number,
#             data,
#             currency,
#             country,
#         )

#         # Step 5: Update Plan, Account, and Profile
#         self._update_plan_and_account(
#             plan, account, transaction, phone_number, data, profile
#         )

#         # Step 6: Handle Referrals if Applicable
#         self._handle_referrals(transaction, profile, data, phone_number, currency)

#         return JsonResponse(
#             {"success": True, "url": reverse_lazy("subscriptions:list")}
#         )

#     # Helper Methods
#     def _retrieve_basic_data(self, data, profile):
#         """Retrieve and set default values for basic data fields."""
#         phone_number = data.get("phone_number", profile.user.email)
#         currency = data.get("currency", "KES")
#         country = data.get("country", "Kenya")
#         return phone_number, currency, country

#     def _retrieve_transaction_objects(self, profile, kwargs):
#         """Retrieve pool, account, and plan objects needed for the transaction."""
#         pool = Pool.objects.get(profile=profile, pk=kwargs.get("pool_id"))
#         account = Account.objects.get(pool=pool, pk=kwargs.get("account_id"))
#         plan = Plan.objects.get(account=account, pk=kwargs.get("plan_id"))
#         return pool, account, plan

#     def _is_plan_already_added(self, profile, plan):
#         """Check if the plan is already added to the profile."""
#         return profile.plans.filter(pk=plan.pk).exists()

#     def _calculate_amounts(self, data, pool, account, plan):
#         """Calculate total investment and discount amounts."""
#         total_investment = data.get(
#             "amount", sum(instance.type.price for instance in [pool, account, plan])
#         )
#         discount_price = data.get(
#             "discount_price", Decimal("0.0") * Decimal(total_investment)
#         )
#         return total_investment, discount_price

#     def _create_transaction(  # noqa: PLR0913
#         self, profile, account, amount, discount, phone_number, data, currency, country
#     ):
#         """Create a transaction with provided details."""
#         return self.create_transaction_method(
#             profile=profile,
#             account=account,
#             amount=amount,
#             discount=discount,
#             payment_phone=phone_number,
#             mpesa_transaction_code=data.get("mpesa_transaction_code"),
#             currency=currency,
#             country=country,
#         )

#     def _update_plan_and_account(  # noqa: PLR0913
#         self,
#         plan,
#         account,
#         transaction,
#         phone_number,
#         data,
#         profile,
#     ):
#         """
#         Update plan, account, and profile after a successful transaction.

#         Args:
#             plan: The plan to be updated.
#             account: The account associated with the plan.
#             transaction: The transaction details.
#             phone_number: The payment phone number.
#             data: The data payload containing transaction information.
#             profile: The profile associated with the user.
#         """
#         # Update plan transaction details
#         plan.mpesa_transaction_code = data.get("mpesa_transaction_code")
#         plan.payment_phone_number = phone_number
#         plan.save()

#         # Update account balance
#         account.balance += Decimal(transaction.paid)
#         account.save()

#         # Only add the plan to profile if it is not already included
#         if not profile.plans.filter(pk=plan.pk).exists():
#             profile.plans.add(plan)

#         # Set subscription status
#         profile.is_subscribed = True

#         # Apply waiting verification only if the transaction source is "Account Registration"
#         if transaction.source == "Account Registration":
#             profile.is_waiting_plan_verification = True
#         profile.save()

#     def _handle_referrals(self, transaction, profile, data, phone_number, currency):
#         """
#         Handle referral account updates if the transaction is
#         due to an account registration."""
#         transaction.source = data.get("source", "Account Top Up")
#         if transaction.source == "Account Registration" and profile.referred_by:
#             self._update_referrer_account(
#                 profile, data.get("mpesa_transaction_code"), phone_number, currency
#             )

#     def _update_referrer_account(
#         self,
#         profile,
#         mpesa_code,
#         phone_number,
#         currency="KES",
#         country="Kenya",
#     ):
#         """
#         Updates the referrer's account with referral earnings if the user was
#         referred by another profile and there isn't already a transaction with
#         source="Account Registration".
#         """
#         referrer_profile = profile.referred_by.profile_user
#         referrer_account = Account.objects.get(pool__profile=referrer_profile)

#         # Check if a transaction with source="Account Registration"
#         # exists for this referrer
#         existing_transaction = Transaction.objects.filter(
#             profile=referrer_profile,
#             source="Account Registration",
#         ).exists()

#         # Only update if no "Account Registration" transaction exists
#         if existing_transaction:
#             # Calculate referral earnings
#             interest_earned = Decimal("0.4") * Decimal(
#                 Transaction.objects.create(profile=profile).paid
#             )

#             # Create referral transaction
#             referral_transaction = Transaction.objects.create(
#                 profile=referrer_profile,
#                 account=referrer_account,
#                 type="DEPOSIT",
#                 amount=interest_earned,
#                 discount=Decimal("0.00"),
#                 source="Referral Earnings",
#                 mpesa_transaction_code=mpesa_code,
#                 payment_phone_number=phone_number,
#                 currency=currency,
#                 country=country,
#             )
#             referral_transaction.save()

#             # Update referrer account balance
#             referrer_account.balance += referral_transaction.paid
#             referrer_account.save()
