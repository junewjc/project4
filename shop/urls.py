from django.urls import path, include
from .views import ItemDetailView, HomeView, search, cables, powerbanks, earphones

app_name = 'shop'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('search/', search, name='search'),
    path('cables/', cables, name='cables'), 
    path('powerbanks/', powerbanks, name='powerbanks'),
    path('earphones/', earphones, name='earphones'),
]