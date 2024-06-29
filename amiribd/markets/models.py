from django.db import models

# Create your models here.
class Package(models.Model):
    name = models.CharField(max_length=100, unique=True)
    monthly_price = models.DecimalField(decimal_places=2, max_digits=12)
    annual_price = models.DecimalField(decimal_places=2, max_digits=12)
    monthly_discount = models.PositiveIntegerField(default=3)
    annual_discount = models.PositiveIntegerField(default=15)


    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Package"
        verbose_name_plural = "Packages"


    
