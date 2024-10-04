from django.shortcuts import get_object_or_404
from .models import ShopItem, ShopItemOffer
from django import forms
from unfold.widgets import UnfoldAdminTextInputWidget, UnfoldAdminDecimalFieldWidget
from unfold.contrib.forms.widgets import WysiwygWidget


class ShopItemForm(forms.ModelForm):
    class Meta:
        model = ShopItem
        fields = [
            'title',
            "regular_price",
            "sales_price",
            "description",
        ]

        widgets = {
            "title": UnfoldAdminTextInputWidget(attrs={'placeholder':'Product or item title', 'autofocus':True, 'class':'form-control form-control-lg'}),
            'regular_price': forms.NumberInput(attrs={'placeholder':'Kshs 0.00', 'autofocus':True, 'class':'form-control form-control-lg'}),
            'sales_price': forms.NumberInput(attrs={'placeholder':'Kshs 0.00', 'autofocus':True, 'class':'form-control form-control-lg'}),
            'description': forms.Textarea(attrs={'placeholder':'Product description','class':'form-control', 'rows':2})
        }
        labels = {
            "title": "Product Title",
            'regular_price':"Reqular Price",
            "description": "Extra Info",
            "sales_price":"Sales Price",
        }
        help_text = {
            "description": "Simple Description about your item or product",
        }


class ShopItemOfferForm(forms.ModelForm):
    class Meta:
        model = ShopItemOffer
        fields = [
            'price_offer',
            "email_or_phone",
            "message"
        ]
        widgets = {
            'price_offer': forms.NumberInput(attrs={'placeholder':'Kshs 0.00', 'autofocus':True, 'class':'form-control form-control-lg'}),
            'email_or_phone': forms.TextInput(attrs={'placeholder':'Phone number or email address', 'autofocus':True, 'class':'form-control form-control-lg'}),
            'message': forms.Textarea(attrs={'placeholder':'Enter message here. To help protect your privacy, don’t include personal info.','class':'form-control no-resize', "name":"shop_item_offer_message"})
        }
        labels = {
            "price_offer": "Your price offer",
            "email_or_phone": "Contact channel"
        }

    def __ini__(self, *args, **kwargs):
        # self.request = kwargs.pop("request", None)
        # self.item_id = kwargs.pop("item_id", None)
        super(ShopItemOfferForm, self).__init__(*args, **kwargs)

    # def get_shop_item(self):
    #     item = get_object_or_404(ShopItem, pk=self.item_id)
    #     return item
    # def get_client_profile(self):
    #     return self.request.user.profile_user
    

    # def save(self,commit=True):
    #     # if commit:
    #     #     self.instance.save()
    #     # else:
    #     #     self.instance.client=self.get_client_profile()
    #     #     self.instance.shop_item=self.get_shop_item()
    #     #     self.instance.save()
    #     return self.instance
    
    

        

