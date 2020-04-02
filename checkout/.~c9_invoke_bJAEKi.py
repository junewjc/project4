from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Order, Charge, Transaction, LineItem
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
    

# def get_total(self):
#     total = 0
#     for order_item in self.items.all():
#         total += order_item.get_final_price()
#     return total

def calculate_cart_cost(request):
    all_cart_items = OrderItem.objects.filter(user=request.user)
    amount = 0
    for cart_item in all_cart_items:
        amount += cart_item.item.price * cart_item.quantity
        
    return amount

def products(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "products.html", context)
    
# def checkout(request):
#     total_cost = calculate_cart_cost(request)
   
        
#     return render(request, 'checkout:checkout', {
#         'total_cost':total_cost/100
#     })

def charge(request):
    amount = calculate_cart_cost(request)
    order = Order.objects.filter(user=request.user)
    all_cart_items = OrderItem.objects.filter(user=request.user)
    
    if request.method == 'GET':
        # to create and save a new transaction
        transaction = Transaction()
        transaction.user = request.user
        # transaction.cart_items = CartItem.objects.filter(owner=request.user)
        transaction.status = 'pending'
        transaction.date = timezone.now()
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
            
        
        order_form = CheckoutForm()
        payment_form = PaymentForm()
        return render(request, 'payment.html', {
            'order_form' : order_form,
            'payment_form' : payment_form,
            'amount' : amount,
            'transaction': transaction,
            'order': order,
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
        
        order_form = CheckoutForm(request.POST)
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
                        line_items.product.quantity -=1 
                        line_items.product.save()
                        
                    # to delete all items in the cart
                    cart_items = OrderItem.objects.filter(user=request.user).delete()
                    messages.success(request, "Your order was successful!")
                    return redirect("/")
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
    
    # if request.method == 'GET':
    #     checkout_form = CheckoutForm()
    #     payment_form = PaymentForm()
    #     return render(request, 'payment.html', {
    #         'checkout_form' : checkout_form,
    #         'payment_form' : payment_form,
    #         'amount' : amount,
    #         'order': order,
    #         'all_cart_items': all_cart_items,
    #         'publishable': settings.STRIPE_PUBLISHABLE_KEY
    #     })
    # else:
    #     stripeToken = request.POST['stripe_id']
        
    #     # set the secret key for the Stripe API
    #     stripe.api_key = settings.STRIPE_SECRET_KEY
        
    #     checkout_form = CheckoutForm(request.POST)
    #     payment_form = PaymentForm(request.POST)
        
    #     if checkout_form.is_valid() and payment_form.is_valid():
    #         try:
    #             customer = stripe.Charge.create(
    #                 amount= int(request.POST['amount'])*100,
    #                 currency='usd',
    #                 description='Payment',
    #                 card=stripeToken
    #                 )
                    
    #             if customer.paid:
                    
    #                 order = checkout_form.save(commit=False)
    #                 order.date=timezone.now()
    #                 order.save()
    #                 messages.success(request, "Your order was successful!")
    #                 return redirect("/")
    #             else:
    #                 messages.error(request, "Your card has been declined")
    #                 return redirect('payment.html')
    #         except stripe.error.CardError:
    #                 messages.error(request, "Your card was declined!")
    #                 return redirect('payment.html')
            
    #     else:
    #          return render(request, 'payment.html', {
    #         'checkout_form' : checkout_form,
    #         'payment_form' : payment_form,
    #         'amount' : amount,
    #         'order': order,
    #         'all_cart_items': all_cart_items,
    #         'publishable': settings.STRIPE_PUBLISHABLE_KEY
    #     })
        
    #     return render(request, 'payment.html', {
    #         'checkout_form' : checkout_form,
    #         'payment_form' : payment_form,
    #         'amount' : amount,
    #         'order': order,
    #         'all_cart_items': all_cart_items,
    #         'publishable': settings.STRIPE_PUBLISHABLE_KEY
    #         })


# class CheckoutView(View):
#     def get(self, *args, **kwargs):
#         try:
#             order = Order.objects.get(user=self.request.user, ordered=False)
#             form = CheckoutForm()
#             context = {
#                 'form': form,
#                 'order': order,
#             }

#             shipping_address_qs = Address.objects.filter(
#                 user=self.request.user,
#                 address_type='S',
#                 default=True
#             )

#             billing_address_qs = Address.objects.filter(
#                 user=self.request.user,
#                 address_type='B',
#                 default=True
#             )

#             return render(self.request, "checkout.html", context)
#         except ObjectDoesNotExist:
#             messages.info(self.request, "You do not have an active order")
#             return redirect("checkout:checkout")

#     def post(self, *args, **kwargs):
#         form = CheckoutForm(self.request.POST or None)
#         try:
#             order = Order.objects.get(user=self.request.user, ordered=False)
#             if form.is_valid():

#                 use_default_shipping = form.cleaned_data.get(
#                     'use_default_shipping')
#                 if use_default_shipping:
#                     print("Using the defualt shipping address")
#                     address_qs = Address.objects.filter(
#                         user=self.request.user,
#                         address_type='S',
#                         default=True
#                     )
#                     if address_qs.exists():
#                         shipping_address = address_qs[0]
#                         order.shipping_address = shipping_address
#                         order.save()
#                     else:
#                         messages.info(
#                             self.request, "No default shipping address available")
#                         return redirect('checkout:checkout')
#                 else:
#                     print("User is entering a new shipping address")
#                     shipping_address1 = form.cleaned_data.get(
#                         'shipping_address')
#                     shipping_address2 = form.cleaned_data.get(
#                         'shipping_address2')
#                     shipping_country = form.cleaned_data.get(
#                         'shipping_country')
#                     shipping_zip = form.cleaned_data.get('shipping_zip')

#                     if is_valid_form([shipping_address1, shipping_country, shipping_zip]):
#                         shipping_address = Address(
#                             user=self.request.user,
#                             street_address=shipping_address1,
#                             apartment_address=shipping_address2,
#                             country=shipping_country,
#                             zip=shipping_zip,
#                             address_type='S'
#                         )
#                         shipping_address.save()

#                         order.shipping_address = shipping_address
#                         order.save()

#                         set_default_shipping = form.cleaned_data.get(
#                             'set_default_shipping')
#                         if set_default_shipping:
#                             shipping_address.default = True
#                             shipping_address.save()

#                     else:
#                         messages.info(
#                             self.request, "Please fill in the required shipping address fields")

#                 use_default_billing = form.cleaned_data.get(
#                     'use_default_billing')
#                 same_billing_address = form.cleaned_data.get(
#                     'same_billing_address')

#                 if same_billing_address:
#                     billing_address = shipping_address
#                     billing_address.pk = None
#                     billing_address.save()
#                     billing_address.address_type = 'B'
#                     billing_address.save()
#                     order.billing_address = billing_address
#                     order.save()

#                 elif use_default_billing:
#                     print("Using the defualt billing address")
#                     address_qs = Address.objects.filter(
#                         user=self.request.user,
#                         address_type='B',
#                         default=True
#                     )
#                     if address_qs.exists():
#                         billing_address = address_qs[0]
#                         order.billing_address = billing_address
#                         order.save()
#                     else:
#                         messages.info(
#                             self.request, "No default billing address available")
#                         return redirect('checkout:checkout')
#                 else:
#                     print("User is entering a new billing address")
#                     billing_address1 = form.cleaned_data.get(
#                         'billing_address')
#                     billing_address2 = form.cleaned_data.get(
#                         'billing_address2')
#                     billing_country = form.cleaned_data.get(
#                         'billing_country')
#                     billing_zip = form.cleaned_data.get('billing_zip')

#                     if is_valid_form([billing_address1, billing_country, billing_zip]):
#                         billing_address = Address(
#                             user=self.request.user,
#                             street_address=billing_address1,
#                             apartment_address=billing_address2,
#                             country=billing_country,
#                             zip=billing_zip,
#                             address_type='B'
#                         )
#                         billing_address.save()

#                         order.billing_address = billing_address
#                         order.save()

#                         set_default_billing = form.cleaned_data.get(
#                             'set_default_billing')
#                         if set_default_billing:
#                             billing_address.default = True
#                             billing_address.save()

#                     else:
#                         messages.info(
#                             self.request, "Please fill in the required billing address fields")

#                 payment_option = form.cleaned_data.get('payment_option')

#                 if payment_option == 'S':
#                     return redirect('checkout:payment', payment_option='stripe')
#                 elif payment_option == 'P':
#                     return redirect('checkout:payment', payment_option='paypal')
#                 else:
#                     messages.warning(
#                         self.request, "Invalid payment option selected")
#                     return redirect('checkout:checkout')
#         except ObjectDoesNotExist:
#             messages.warning(self.request, "You do not have an active order")
#             return redirect("cart:order-summary")


# class PaymentView(View):
#     def get(self, *args, **kwargs):
#         order = Order.objects.get(user=self.request.user, ordered=False)
#         if order.billing_address:
#             context = {
#                 'order': order,
#                 'STRIPE_PUBLISHABLE_KEY':settings.STRIPE_PUBLISHABLE_KEY
#             }
#             return render(self.request, "payment.html", context)
#         else:
#             messages.warning(
#                 self.request, "You have not added a billing address")
#             return redirect("checkout:checkout")

#     def post(self, *args, **kwargs):
#         order = Order.objects.get(user=self.request.user, ordered=False)
#         form = PaymentForm(self.request.POST)
        
#         if form.is_valid():
#             token = form.cleaned_data.get('stripeToken')
#             save = form.cleaned_data.get('save')
#             use_default = form.cleaned_data.get('use_default')

#             amount = int(order.get_total() * 100)

#             try:

#                 # create the payment
#                 payment = Payment()
#                 payment.user = self.request.user
#                 payment.amount = order.get_total()
#                 payment.save()

#                 # assign the payment to the order

#                 order_items = order.items.all()
#                 order_items.update(ordered=True)
#                 for item in order_items:
#                     item.save()

#                 order.ordered = True
#                 order.payment = payment
#                 order.ref_code = create_ref_code()
#                 order.save()

#                 messages.success(self.request, "Your order was successful!")
#                 return redirect("/")

#             except stripe.error.StripeError as e:
#                 # Display a very generic error to the user, and maybe send
#                 # yourself an email
#                 messages.warning(
#                     self.request, "Something went wrong. You were not charged. Please try again.")
#                 return redirect("/")

#         messages.warning(self.request, "Invalid data received")
#         return redirect("/payment/stripe/")

