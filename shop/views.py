from django.shortcuts import render
from shop.models import Item 
from checkout.models import OrderItem
from django.views.generic import ListView, DetailView, View
from django.db.models import Q
from django.shortcuts import get_object_or_404
# Create your views here.

def calculate_no_of_items(request):
    all_cart_items = OrderItem.objects.filter(user=request.user)
    count = 0
    for cart_item in all_cart_items:
        count += 1
    return count

def products(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "product.html", context)
    
def ItemDetailView(request, id=None):
    item = get_object_or_404(Item, id=id)

    context = {
        "item": item
    }
    return render(request, "product.html", context)    
    
    
class HomeView(ListView):
    model = Item
    paginate_by = 50
    template_name = "home.html"
 

def cables(request):
    items = Item.objects.filter(category='PC')
    return render(request, "filter.html",  {'items': items})
    
def powerbanks(request):
    items = Item.objects.filter(category='PB')
    return render(request, "filter.html",  {'items': items})
    
def earphones(request):
    items = Item.objects.filter(category='EP')
    return render(request, "filter.html",  {'items': items})
    
    
def search(request):
    query = request.GET.get('q')
    products=Item.objects.filter(name__icontains=query)
    return render(request, "search.html", {'products': products, 'query':query})

