from django.db import models
from django.conf import settings

# Create your models here.

CATEGORY_CHOICES = (
    ('PC', 'Phone Cables'),
    ('PB', 'Power Banks'),
    ('EP', 'Earphone')
)


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(upload_to='images/', null=True)

    def __str__(self):
        return self.title