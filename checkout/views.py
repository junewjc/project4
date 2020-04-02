from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Charge, Transaction, LineItem
from shop.models import Item
from cart.models import OrderItem
from django.views.generic import ListView, DetailView, View
from .forms import OrderForm, PaymentForm
import string
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.

def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid


def calculate_cart_cost(request):
    all_cart_items = OrderItem.objects.filter(user=request.user)
    amount = 0
    for cart_item in all_cart_items:
        amount += cart_item.item.price * cart_item.quantity
    return amount
    
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
    return render(request, "products.html", context)
    

def charge(request):
    amount = calculate_cart_cost(request)
    count = calculate_no_of_items(request)
    
    if request.method == 'GET':
        # to create and save a new transaction
        transaction = Transaction()
        transaction.user = request.user
        # transaction.cart_items = OrderItem.objects.filter(owner=request.user)
        transaction.date = timezone.now()
        transaction.status = 'pending'
        transaction.save()
        
        # to retrive and save the details of the cart items into line item model
        all_cart_items = OrderItem.objects.filter(user=request.user)
        for cart_items in all_cart_items:
            lineItem = LineItem()
            lineItem.transaction = transaction
            lineItem.item = cart_items.item
            lineItem.title = cart_items.item.title
            lineItem.sku = cart_items.item.sku
            lineItem.price = cart_items.item.price
            lineItem.save()
            
        
        order_form = OrderForm()
        payment_form = PaymentForm()
        return render(request, 'payment.html', {
            'order_form' : order_form,
            'payment_form' : payment_form,
            'amount' : amount,
            'count' : count,
            'transaction': transaction,
            'all_cart_items': all_cart_items,
            'publishable': settings.STRIPE_PUBLISHABLE_KEY
        })
    else:
        
        transaction_id = request.POST['transaction_id']
        transaction = Transaction.objects.get(pk=transaction_id)
        if transaction.status != 'pending':
            return HttpResponse("The session has expired.")
        
        #to process the payment
        stripeToken = request.POST['stripe_id']
        
        # set the secret key for the Stripe API
        stripe.api_key = settings.STRIPE_SECRET_KEY
        
        order_form = OrderForm(request.POST)
        payment_form = PaymentForm(request.POST)
        
        if order_form.is_valid() and payment_form.is_valid():
            try:
                
                customer = stripe.Charge.create(
                    amount= int(amount*100),
                    currency='usd',
                    description=request.user.email,
                    card=stripeToken
                    )
                    
                if customer.paid:
                    
                    order = order_form.save(commit=False)
                    order.date=timezone.now()
                    order.save()
                    
                    # to update the transaction status after payment has been made
                    transaction.status = 'approved'
                    transaction.charge = order
                    transaction.save()
                    
                    # to update the inventory
                    line_items = LineItem.objects.filter(transaction_id=transaction.id)
                    for each_line_item in line_items:
                        each_line_item.item.quantity -=1 
                        each_line_item.item.save()
                        
                    # to delete all items in the cart
                    cart_items = OrderItem.objects.filter(user=request.user).delete()
                    messages.success(request, "Your order was successful!")
                    return render(request, "payment-success.html")
                else:
                    messages.error(request, "Your card has been declined")
            except stripe.error.CardError:
                    messages.error(request, "Your card was declined!")
            
        else:
             return render(request, 'checkout.html', {
            'order_form' : order_form,
            'payment_form' : payment_form,
            'amount' : amount,
            'order': order,
            'all_cart_items': all_cart_items,
            'publishable': settings.STRIPE_PUBLISHABLE_KEY
        })
        
        return render(request, 'checkout.template.html', {
            'order_form' : order_form,
            'payment_form' : payment_form,
            'amount' : amount,
            'order': order,
            'all_cart_items': all_cart_items,
            'publishable': settings.STRIPE_PUBLISHABLE_KEY
            })
    

