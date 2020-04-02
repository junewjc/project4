from django.urls import path, include
from .views import add_to_cart, remove_from_cart, remove_single_item_from_cart, view_cart

app_name = 'cart'

urlpatterns = [
    path('order-summary/', view_cart, name='order-summary'),
    path('add-to-cart/<id>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<id>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<id>/', remove_single_item_from_cart, name='remove-single-item-from-cart'),
]