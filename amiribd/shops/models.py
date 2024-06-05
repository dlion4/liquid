from django.db import models
from amiribd.invest.models import generate_ssid
from amiribd.users.models import Profile
import random, string
from django.utils import timezone
# Create your models here.

def generate_item__ssid(instance, k=20):
    char = "".join(
        random.choices(
            str(
                str(instance.pk)
                + str(instance.profile.pk)
                + string.ascii_uppercase
                + string.digits
            ),
            k=k,
        )
    )

    return char



class ShopItem(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile_sale_items")
    title = models.CharField(max_length=100)
    regular_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    sales_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    description = models.TextField()
    item_ssid = models.CharField(blank=True, max_length=100, null=True)
    is_sold = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sold_at = models.DateTimeField(blank=True, null=True)
    sold_to = models.ForeignKey(Profile, blank= True, null=True, on_delete=models.SET_NULL)
    discount = models.GeneratedField(
        expression=(models.F("regular_price")-models.F("sales_price")),
        output_field = models.DecimalField(max_digits=12, decimal_places=2, default=0.00),
        db_persist = True
    )
    def __str__(self):
        return str(self.title)
    

    def save(self, *args, **kwargs):
        if not self.item_ssid:
            self.item_ssid = generate_item__ssid(self)
        super().save(*args, **kwargs)
    
    

class ShopItemOffer(models.Model):
    client = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="shop_item_offer_client")
    shop_item = models.ForeignKey(ShopItem, on_delete=models.CASCADE, related_name="shop_item_offer")
    message = models.TextField()
    price_offer = models.DecimalField(decimal_places=2, max_digits=12, default=0.00)
    email_or_phone = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Offer Id {self.pk}"