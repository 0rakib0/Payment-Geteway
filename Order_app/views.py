from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from Order_app.models import Cart, Order
from Shop_app.models import Product
from django.contrib import messages

# Create your views here.


@login_required
def Add_to_cart(request, id):
    item = get_object_or_404(Product, pk=id)
    Order_item = Cart.objects.get_or_create(item=item, user=request.user, purchased=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.order_items.filter(item=item).exists():
            Order_item[0].quatity +=1
            Order_item[0].save()
            messages.info(request, 'This item quantity was updated!')
            return redirect('Shop_App:home')
        else:
            order.order_items.add(Order_item[0])
            messages.info(request, 'This item was added successfully!')
            return redirect('Shop_App:home')
    else:
       order = Order(user=request.user)
       order.save()
       order.order_items.add(Order_item[0])
       messages.info(request, 'Product wass successsfully added')
       return redirect('Shop_App:home')

@login_required
def Cart_view(request):
    carts = Cart.objects.filter(user=request.user, purchased=False)
    orders = Order.objects.filter(user=request.user, ordered=False)

    if carts.exists() and orders.exists():
        order = orders[0]
        return render(request, 'Order_app/cart.html', context={'carts':carts, 'order':order})
    
    else:
        messages.info(request, 'You dont have no item in your carts')
        return redirect('Shop_App:home')


@login_required
def remove_from_cart(request, pk):
    item = Product.objects.get(pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.order_items.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            order.order_items.remove(order_item)
            order_item.delete()
            messages.info(request, 'This item is remove from your cart!')
            return redirect('Order_App:carts')
    else:
        messages.info(request, "You don't have any active order!")
        return redirect('Shop_App:home')

def increase(request, pk):
    item = Product.objects.get(pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.order_items.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            if order_item.quatity >=1:
                order_item.quatity +=1
                order_item.save()
                messages.info(request, 'Item successfully updated')
                return redirect('Order_App:carts')
        else:
            messages.info(request, f"{item.name} is not in your cart!")
            return redirect('Shop_App:home')
    
    else:
        messages.info(request, "You dn't have an active order")
        return redirect('Shop_App:home')

def dicress(request, pk):
    item = Product.objects.get(pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.order_items.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            if order_item.quatity > 1:
                order_item.quatity -=1
                order_item.save()
                messages.info(request, 'Item successfully updated')
                return redirect('Order_App:carts')
            else:
                order.order_items.remove(order_item)
                order_item.delete()
                messages.warning(request, 'Item remove from your cart!')
                return redirect('Shop_App:home')
        else:
            messages.info(request, f"{item.name} is not in your cart!")
            return redirect('Shop_App:home')
    
    else:
        messages.info(request, "You dn't have an active order")
        return redirect('Shop_App:home')
