from django.urls import path
from .views import OrderList , checkout ,add_to_cart , remove_from_cart , order_summary , mpesa_initiate_payment,mpesa_payment_success,mpesa_payment_failed , mpesa_callback , check_transaction_status

from .api import CartDetailCreateAPI , OrderListAPI , OrderDetailAPI , CreateOrderAPI , ApplyCouponAPI 



app_name = 'orders'

urlpatterns = [
    path('', OrderList.as_view()),
    path('checkout',checkout),
    path('add_to_cart', add_to_cart ,name ='add_to_cart'),
    path('<int:id>/remove-from-cart',remove_from_cart),
    path('order-summary/', order_summary, name='order_summary'),
    #mpesa integrations

    path('order/<int:order_id>/mpesa/', mpesa_initiate_payment, name='mpesa_initiate_payment'),
    path('api/mpesa-callback/', mpesa_callback, name='mpesa_callback'),
    path('order/mpesa/success/', mpesa_payment_success, name='mpesa_payment_success'),
    path('order/mpesa/failed/', mpesa_payment_failed, name='mpesa_payment_failed'),
    path('mpesa/check-status/<str:checkout_request_id>/', check_transaction_status, name='mpesa_check_status'),


    # api  
    path('api/list/<str:username>',OrderListAPI.as_view()),
    path('api/list/<str:username>/create-order',CreateOrderAPI.as_view()),
    path('api/<str:username>/cart', CartDetailCreateAPI.as_view()),
    path('api/<str:username>/cart/apply-coupon', ApplyCouponAPI.as_view()),
    path('api/list/<str:username>/<int:pk>',OrderDetailAPI.as_view()),
]
