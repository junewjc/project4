from django.urls import path, include
from .views import CheckoutView

urlpatterns = [
    path('', CheckoutView, name='checkout'),
]