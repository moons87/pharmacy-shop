from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .models import Cart, CartItem
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from pharmacy.models import Pharmacy, PharmacyProductPrice
from functools import wraps


# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart



def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id) # получить товар
    # Если пользователь авторизован
    if current_user.is_authenticated:
        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.get(product=product, user=current_user)
            cart_item.quantity += 1 # cart_item.quantity = cart_item.quantity +1
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                user=current_user,
            )


        cart_item.save()
        return redirect('cart')

    # Если пользователь не авторизован
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request)) # получить корзину с использованием cart_id в сессии
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
        cart.save()

        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.get(product=product, cart=cart)
            cart_item.quantity += 1 # cart_item.quantity = cart_item.quantity +1
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,
            )


        

        cart_item.save()
        return redirect('cart')


    

def remove_cart(request, product_id, cart_item_id):
    
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id = cart_item_id)
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))  
            cart_item = CartItem.objects.get(product=product, cart=cart, id = cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id = cart_item_id)
    else:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_item  = CartItem.objects.get(product=product, cart=cart, id = cart_item_id)
    cart_item.delete()
    return redirect('cart')



def cart(request, total = 0, quantity =0, cart_items = None):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active = True).order_by('id')
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active = True).order_by('id')
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        
    except ObjectDoesNotExist:
        pass # just ignore
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items':cart_items,
    }
    return render(request, 'store/cart.html', context)


@login_required(login_url='login')


def checkout(request, total = 0, quantity =0, cart_items = None):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active = True).order_by('id')
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active = True).order_by('id')
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
    except ObjectDoesNotExist:
        pass # just ignore
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items':cart_items
    }
    return render(request, 'store/checkout.html', context)
    
 