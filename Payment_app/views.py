from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse
from Order_app.models import Order, Cart
from Payment_app.models import Billing_address
from Payment_app.forms import Billing_form
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# for payment
import requests
from sslcommerz_python.payment import SSLCSession
from decimal import Decimal
import socket
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def Checkout(request):
    save_address = Billing_address.objects.get_or_create(user=request.user)
    save_address = save_address[0]
    form = Billing_form(instance=save_address)
    if request.method == 'POST':
        form = Billing_form(request.POST, instance=save_address)
        if form.is_valid():
            form.save()
            form = Billing_form(instance=save_address)
            messages.success(request, 'Billing address successfully saved!')
    order_qs = Order.objects.filter(user=request.user)
    order_item = order_qs[0].order_items.all()
    order_total = order_qs[0].get_totals()
    return render(request, 'Pyment_app/checkout.html', context={'form':form, 'order_item':order_item, 'order_total':order_total, 'save_address':save_address})

@login_required
def Payment(request):
    saved_address = Billing_address.objects.get_or_create(user=request.user)
    saved_address = saved_address[0]
    if not saved_address.fully_field():
        messages.info(request, 'Please filup your shipping address!')
        return redirect('Order_App:carts')
    if not request.user.profile.is_fully_filed():
        messages.info(request, 'Please fillup your full information in profile!')
        return redirect('Auth_App:profile')
     
    store_id = 'rrras6377c57e6e7b1'
    API_key = 'rrras6377c57e6e7b1@ssl'
    mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id, sslc_store_pass=API_key)
    status_url = request.build_absolute_uri(reverse('Payment_App:status'))
    mypayment.set_urls(success_url=status_url, fail_url=status_url, cancel_url=status_url, ipn_url=status_url)
    
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_items = order_qs[0].order_items.all()
    order_items_count = order_qs[0].order_items.count()
    order_total = order_qs[0].get_totals()


    mypayment.set_product_integration(total_amount=Decimal(order_total), currency='BDT', product_category='Mixed', product_name=order_items, num_of_item=order_items_count, shipping_method='Kuriar', product_profile='None')

    corrent_user = request.user

    mypayment.set_customer_info(name=corrent_user.profile.full_name, email=corrent_user.email, address1=corrent_user.profile.address_1, address2=corrent_user.profile.address_1, city=corrent_user.profile.city, postcode=corrent_user.profile.zipcode, country=corrent_user.profile.country, phone=corrent_user.profile.phone)

    mypayment.set_shipping_info(shipping_to=corrent_user.profile.full_name, address=saved_address.address, city=saved_address.city, postcode=saved_address.zipcode, country=saved_address.country)

    response_data = mypayment.init_payment()

    return redirect(response_data['GatewayPageURL'])

@csrf_exempt
def Complate(request):
    if request.method == 'POST' or request.method == 'post':
        payment_data = request.POST
        status = payment_data['status']

        if status == 'VALID':
            val_id = payment_data['val_id']
            tran_id = payment_data['tran_id']
            messages.success(request, 'Your payment Coplated successfully!')
            return HttpResponseRedirect(reverse('Payment_App:purchase', kwargs={'val_id':val_id, 'tran_id':tran_id}))

        if status == 'FAILED':
            messages.warning(request, 'Your payment Do not Coplated successfully! Try again')


    return render(request, 'Pyment_app/complate.html', context={})



@login_required
def Purchase(request, val_id, tran_id):
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order = order_qs[0]
    orderId = tran_id
    order.ordered=True
    order.orderID=orderId
    order.paymentID=val_id
    order.save()
    cart_item = Cart.objects.filter(user=request.user, purchased=False)
    for item in cart_item:
        item.purchased = True
        item.save()
    return HttpResponseRedirect(reverse("Shop_App:home"))


@login_required
def Order_view(request):
    try:
        orders = Order.objects.filter(user=request.user, ordered=True)
        context = {
            'orders':orders
        }
    except:
        messages.warning(request, 'You do no have an active order')
        return redirect('Shop_App:home')
    return render(request, 'Pyment_app/order.html', context)