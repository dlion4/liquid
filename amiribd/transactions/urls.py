from django.urls import reverse, path

app_name = "transaction"
from  . import views


urlpatterns = [
    path("filter/", views.TransactionFilterView.as_view(), name="filter-transaction")
]