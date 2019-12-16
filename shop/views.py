from django.shortcuts import render
from shop.models import Item
from django.views.generic import ListView, DetailView, View
from django.db.models import Q
# Create your views here.

def products(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "product.html", context)
    
    
class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"
    
    
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

