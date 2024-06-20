from django.db import models

# Create your models here.

class KenyaConversion(models.Model):
    currency = models.CharField(max_length=3, default="KES")
    def __str__(self):
        return f"{self.currency}"




class Country(models.Model):
    kenya = models.ForeignKey(KenyaConversion, related_name='countries', on_delete=models.CASCADE)
    country = models.CharField(max_length=100)
    currency_code = models.CharField(max_length=100)
    currency_name = models.CharField(max_length=100, blank=True, null=True)
    amount = models.PositiveIntegerField(default=10, help_text="In relation to 1 KShs")
    conversion_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.country} - {self.currency_code}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['kenya','country', 'currency_code'],
                name='unique_kenya_country_currency_code',
                # condition=models.Q(currency_name__isnull=True),
            )
        ]