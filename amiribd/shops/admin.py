from django.contrib import admin
from amiribd.core.admin import earnkraft_site
# Register your models here.
from .models import ShopItem, ShopItemOffer
from .forms import ShopItemForm


@admin.register(ShopItem, site=earnkraft_site)
class ItemAdmin(admin.ModelAdmin):
    form = ShopItemForm
    list_display = [
        "profile",
        "title",
        "regular_price",
        "sales_price",
        "item_ssid",
        "is_sold",
        "created_at",
        "updated_at",
        "sold_at",
        "sold_to",
        "discount"
    ]
    search_fields=[
        'item_ssid',
        "title",
    ]
    list_filter = [
        'is_sold',
         "created_at",
        "updated_at",
        "sold_at",
    ]


@admin.register(ShopItemOffer, site=earnkraft_site)
class ShopItemOfferAdmin(admin.ModelAdmin):
    list_display = [
        "client",
        "shop_item",
        "price_offer",
        "email_or_phone",
        "created_at",
        "updated_at",
    ]
