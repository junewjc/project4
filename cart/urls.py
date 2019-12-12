from django.urls import path, include
from .views import add_to_cart, remove_from_cart, remove_single_item_from_cart, OrderSummaryView

urlpatterns = [
    path('add-to-cart/<slug>/', OrderSummaryView, name='cart'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart, name='remove-single-item-from-cart'),
]