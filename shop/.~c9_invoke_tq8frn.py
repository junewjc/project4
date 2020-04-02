from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.shortcuts import reverse

# Create your models here.

CATEGORY_CHOICES = (
    ('PC', 'Phone Cables'),
    ('PB', 'Power Banks'),
    ('EP', 'Earphone')
)



class Item(models.Model):
    title = models.CharField(max_length=100)
    sku = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    description = models.TextField()
    image = models.ImageField(upload_to='images/', null=True)

    def __str__(self):
        return self.title + " : " + self.sku
        
    
    def get_absolute_url(self):
        return reverse("shop:product", kwargs={
            'id': self.id
        })

    def get_add_to_cart_url(self):
        return reverse("cart:add-to-cart", kwargs={
            'id': self.id
        })

    def get_remove_from_cart_url(self):
        return reverse("cart:remove-from-cart", kwargs={
            'id': self.id
        })
        
