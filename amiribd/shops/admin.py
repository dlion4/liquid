from django.contrib import admin

# Register your models here.
from .models import ShopItem, ShopItemOffer



@admin.register(ShopItem)
class ItemAdmin(admin.ModelAdmin):
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


@admin.register(ShopItemOffer)
class ShopItemOfferAdmin(admin.ModelAdmin):
    list_display = [
        "client",
        "shop_item",
        "price_offer",
        "email_or_phone",
        "created_at",
        "updated_at",
    ]
