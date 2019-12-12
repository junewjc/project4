from django.shortcuts import render
from shop.models import Item
from django.views.generic import ListView, DetailView, View
# Create your views here.

def catalog(request):
    all_products = Item.objects.all();
    return render(request, 'home.template.html',{
        'all_products':all_products
    })