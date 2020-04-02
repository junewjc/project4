from django.urls import path, include
from .views import charge

app_name = 'checkout'

urlpatterns = [
    path('', charge, name='checkout'),
]