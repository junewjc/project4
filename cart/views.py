from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View
from .models import OrderItem
from shop.models import Item
from django.utils import timezone

# Create your views here.



def calculate_cart_cost(request):
    all_cart_items = OrderItem.objects.filter(user=request.user)
    amount = 0
    for cart_item in all_cart_items:
        amount += cart_item.item.price * cart_item.quantity
        
    return amount

@login_required
def view_cart(request):
    amount = calculate_cart_cost(request)
    all_cart_items = OrderItem.objects.filter(user=request.user)
    return render(request, 'order_summary.html',{
            'all_cart_items':all_cart_items,
            'amount':amount
        })

@login_required
def add_to_cart(request, id):

    item = Item.objects.get(id=id)
    existing_cart_item = OrderItem.objects.filter(user=request.user, item=item).first()

    # if the cart item does not exist, create a new one
    if existing_cart_item == None:
        new_cart_item = OrderItem()
        new_cart_item.item = item
        new_cart_item.user = request.user
        new_cart_item.quantity = 1
        new_cart_item.save()
        messages.info(request, "This item quantity was updated.")
        return redirect("cart:order-summary")
    else:
        # increases its quantity
        existing_cart_item.quantity += 1
        existing_cart_item.save()
        messages.info(request, "This item was added to your cart.")
        return redirect("cart:order-summary")
        
        
@login_required
def remove_from_cart(request, id):
    
    item = Item.objects.get(id=id)
    existing_cart_item = OrderItem.objects.filter(user=request.user, item=item).first()
    existing_cart_item.delete()
    messages.info(request, "This item was removed from your cart.")
    return redirect("cart:order-summary")



@login_required
def remove_single_item_from_cart(request, id):
    
    item = Item.objects.get(id=id)
    existing_cart_item = OrderItem.objects.filter(user=request.user, item=item).first()

    if existing_cart_item != None:
        if existing_cart_item.quantity > 1:
            existing_cart_item.quantity -= 1
            existing_cart_item.save()
        else:
            existing_cart_item.delete()
        messages.info(request, "This item quantity was updated.")
        return redirect("cart:order-summary")
        
