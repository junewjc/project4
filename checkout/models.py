from django.db import models
from django.conf import settings
from shop.models import Item
from cart.models import OrderItem
# from django_countries.fields import CountryField
# from django.db.models.signals import post_save
# from django.db.models import Sum

# Create your models here.

class LineItem(models.Model):
    item = models.ForeignKey('shop.item', null=True, on_delete=models.CASCADE)
    sku = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    transaction = models.ForeignKey('Transaction', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.item.name + " : " + self.sku

        
class Charge(models.Model):
    full_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    country = models.CharField(max_length=40)
    postcode = models.CharField(max_length=20)
    town_or_city = models.CharField(max_length=40)
    street_address1 = models.CharField(max_length=40)
    street_address2 = models.CharField(max_length=40)
    date = models.DateField()

    def __str__(self):
        return "{0}-{1}-{2}".format(self.id, self.date, self.full_name)
        
class Transaction(models.Model):
    
    status_options = [
        ('pending', "Pending"),
        ('approved', "Approved"),
        ('rejected', "Rejected"),
        ('shipping', 'Shipping'),
        ('delivered', 'Delivered'),
        ('lost', 'Lost')
    ]
    
    charge = models.ForeignKey('Charge', on_delete=models.CASCADE, null=True)
    status = models.CharField(blank=False, choices=status_options, max_length=50)
    date = models.DateField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return str(self.id)

