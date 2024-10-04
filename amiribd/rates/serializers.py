from  rest_framework import serializers
from .models import KenyaConversion, Country

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"

class KenyaConversionModelSerializer(serializers.ModelSerializer):
    countries = CountrySerializer(many=True)
    class Meta:
        model = KenyaConversion
        fields = ["countries"]