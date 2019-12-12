from django.urls import path, include
from .views import add_to_cart

urlpatterns = [
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
]