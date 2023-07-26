from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from carts.models import CartItem
from .forms import OrderForm
from .models import Order, Payment, OrderProduct
import datetime
from django.contrib import messages
import json
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

@csrf_exempt
def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])
    
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    # Move the cart items to Order Product table
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        cart_item = CartItem.objects.get(id=item.id)
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.save()



        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

        CartItem.objects.filter(user=request.user).delete()

        mail_subject = 'Спасибо за заказ!'
        message = render_to_string('orders/order_recieved_email.html', {
            'user': request.user,
            'order': order,
        })
        to_email = request.user.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()

        # Send order number and transaction id back to sendData method via JsonResponse
        data = {
            'order_number': order.order_number,
            'transID': payment.payment_id,
        }
    return JsonResponse(data)

def place_order(request, total = 0, quantity =0):
    current_user = request.user

    #if the cart count is less than or equal to 0, then redirect back to shop
    cart_items = CartItem.objects.filter(user = current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    grand_total = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    grand_total = total 

    if request.method == 'POST':
        form = OrderForm(request.POST)
        
        if form.is_valid(): 
            data = Order()
            data.user=current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.email = form.cleaned_data['email']
            data.phone = form.cleaned_data['phone']
            data.address_line = form.cleaned_data['address_line']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") 
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user = current_user, is_ordered = False, order_number = order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'grand_total': grand_total   
            }
            return render(request, 'orders/payments.html', context)
            
        else:
            return redirect('checkout')
      

def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')
    payment_method = request.GET.get('payment_method')

    # Если метод оплаты наличными, создайте заказ и платеж
    if payment_method == 'Cash':
        order = Order.objects.create(
            order_number=order_number,
            first_name=request.user.first_name,
            email=request.user.email,
            phone=request.user.phone_number,
            order_total=0,
            is_ordered=True,
        )
        
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        payment = Payment.objects.create(
            user=request.user,
            payment_method='Cash',
            amount_paid=subtotal,
            status='COMPLETED',
            created_at=timezone.now().date(),
        )

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'payment': payment,
            'subtotal': subtotal,
        }
        return render(request, 'orders/payment_cash_on_delivery.html', context)
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        payment = Payment.objects.get(payment_id=transID)

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
        }
        return render(request, 'orders/payment_cash_on_delivery.html', context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')
    

@csrf_exempt
def payment_cash_on_delivery(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        # обработка оплаты наличными при получении
        order.payment_method = 'Cash on delivery'
        order.payment_status = 'Paid'
        order.save()
        messages.success(request, 'Оплата наличными при получении была успешно обработана.')
        return redirect('order_detail', order_id=order_id)
    context = {'order': order}
    return render(request, 'payment_cash_on_delivery.html', context)