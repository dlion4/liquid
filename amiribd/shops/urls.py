
from django.urls import reverse, path, include
from . import views

app_name = "shops"

urlpatterns = [
    path("add-product/", views.ShopItemCreateView.as_view(), name="add-product-item"),
    path("place-offer/<item_id>/", views.ShopItemOfferView.as_view(), name="place-offer-on-item"),
]
