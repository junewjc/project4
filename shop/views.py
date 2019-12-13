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
    paginate_by = 10
    template_name = "home.html"
    
    
    
def search(request):
    item=Item.objects.filter(name__icontains=request.GET['query'])
    return render(request, "home.html", {'all_items':item})