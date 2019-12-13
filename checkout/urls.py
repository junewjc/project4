from django.urls import path, include
from .views import CheckoutView, AddCouponView, PaymentView

app_name = 'checkout'

urlpatterns = [
    path('', CheckoutView.as_view(), name='checkout'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
]