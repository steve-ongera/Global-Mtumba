from django.shortcuts import render , redirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order ,Cart , CartDetail,OrderDetail , Coupon
from product.models import Product
from django.shortcuts import get_object_or_404
from settings.models import DeliveryFee
import datetime

from django.http import JsonResponse
from django.template.loader import render_to_string

class OrderList(LoginRequiredMixin,ListView):
    model = Order
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        return queryset
    




def add_to_cart(request):
    quantity = request.POST['quantity']
    product = Product.objects.get(id=request.POST['product_id'])
    cart = Cart.objects.get(user= request.user , status= 'InProgress')
    cart_detail , created = CartDetail.objects.get_or_create(cart=cart,product=product )
    cart_detail.quantity = int(quantity)
    cart_detail.total = round( int(quantity)* product.price, 2)
    cart_detail.save()
    return redirect(f'/products/{product.slug}')


def remove_from_cart(request,id):
    cart_detail = CartDetail.objects.get(id=id)
    cart_detail.delete()
    return redirect('/products/')



@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user,status='InProgress')
    cart_detail = CartDetail.objects.filter(cart=cart)
    delivery_fee = DeliveryFee.objects.last().fee

    if request.method == 'POST':
        coupon = get_object_or_404(Coupon,code=request.POST['coupon_code'])  # 404


        if coupon and coupon.quantity > 0 :
            today_date = datetime.datetime.today().date()
            # if (coupon.start <= today_date < coupon.end ):
            if today_date >= coupon.start_date and today_date <= coupon.end_date:
                coupon_value = cart.cart_total() * coupon.discount/100
                cart_total = cart.cart_total() - coupon_value

                coupon.quantity -= 1 
                coupon.save()
                cart.coupon = coupon
                cart.total_After_coupon = cart_total
                cart.save()

                total = delivery_fee + cart_total

                cart = Cart.objects.get(user=request.user,status='InProgress')
                

                html = render_to_string('include/checkout_table.html',{
                    'cart_detail' : cart_detail,
                    'sub_total' : cart_total,
                    'cart_total' : total,
                    'coupon' : coupon_value ,
                    'delivery_fee' : delivery_fee
                    
                })
                return JsonResponse({'result':html})



                # return render(request,'orders/checkout.html',{
                #     'cart_detail' : cart_detail,
                #     'sub_total' : cart_total,
                #     'cart_total' : total,
                #     'coupon' : coupon_value ,
                #     'delivery_fee' : delivery_fee
                    
                # })

    # else:
    #     total =  delivery_fee + cart.cart_total()
    #     coupon = 0 ,        

    return render(request ,'orders\checkout.html',
        {
        'cart_detail' : cart_detail,
        'sub_total' : cart.cart_total(),
        'cart_total' : delivery_fee + cart.cart_total(),
        'coupon' : 0,
        'delivery_fee' : delivery_fee
        })


def order_summary(request):
    # Retrieve the user's active cart
    cart = get_object_or_404(Cart, user=request.user, status="InProgress")
    
    # Get or create an order associated with the cart
    order, created = Order.objects.get_or_create(
        user=request.user, 
        status='Received',
        defaults={'total_After_coupon': cart.total_After_coupon or cart.cart_total()}
    )
    
    # Get all cart details (products in the cart)
    cart_details = cart.cart_detail.all()
    
    # Calculate the total price before and after applying the coupon
    total_before_coupon = cart.cart_total()
    total_after_coupon = cart.total_After_coupon if cart.total_After_coupon else total_before_coupon
    
    # Prepare context for the template
    context = {
        'cart': cart,
        'order': order,  # Include the order object in the context
        'cart_details': cart_details,
        'total_before_coupon': total_before_coupon,
        'total_after_coupon': total_after_coupon,
    }
    return render(request, 'orders/order_summary.html', context)



import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import base64
from django.http import HttpResponse, JsonResponse
import datetime
import json
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .models import *


def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])

    # Store transaction details inside Payment model
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
    cart_items = Cart.objects.filter(user=request.user)

    for item in cart_items:
        orderproduct = Order()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        cart_item = Cart.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct = Order.objects.get(id=orderproduct.id)
        orderproduct.save()


        # Reduce the quantity of the sold products
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    # Clear cart
    Cart.objects.filter(user=request.user).delete()

    # Send order recieved email to customer
    mail_subject = 'Thank you for your order!'
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



from orders.models import Order

def create_order_from_cart(user, cart):
    if cart.cart_detail.exists():
        total = cart.cart_total()
        order = Order.objects.create(
            user=user,
            status="Received",
            total_After_coupon=cart.total_After_coupon or total,
        )
        # Transfer cart details to order details
        for item in cart.cart_detail.all():
            OrderDetail.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity,
                total=item.total,
            )
        return order
    return None



#mpesa integration
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order
from .utils import lipa_na_mpesa_online  # Assuming these are defined in utils.py

def mpesa_initiate_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Calculate the total amount of the order by summing the total of each order detail
    order_total = sum(detail.total for detail in order.order_detail.all())

    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        account_reference = f'Order {order.code}'  # Or use order_number if you added it
        transaction_desc = 'Payment for your order'
        
        # Call the M-Pesa API function to initiate payment
        response = lipa_na_mpesa_online(phone_number, order_total, account_reference, transaction_desc)

        if response.get('ResponseCode') == '0':
            # Payment was successful, update order status and notify user
            order.transaction_id = response.get('CheckoutRequestID')
            order.transaction_status = 'Pending'
            order.save()

            # Optionally send an SMS to the user
            #sms_body = f"Thank you for your order! Your payment for Order {order.code} is pending."
            #send_sms(phone_number, sms_body)

            return redirect('orders:mpesa_payment_success')
        else:
            return redirect('orders:mpesa_payment_failed')

    return render(request, 'orders/mpesa.html', {'order': order})


def mpesa_payment_success(request):
    return render(request, 'orders\mpesa_payment_success.html')

def mpesa_payment_failed(request):
    return render(request, 'orders\mpesa_payment_failed.html')
