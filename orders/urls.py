from django.urls import path
from .views import OrderList , checkout ,add_to_cart , remove_from_cart , order_summary , mpesa_initiate_payment,mpesa_payment_success,mpesa_payment_failed

from .api import CartDetailCreateAPI , OrderListAPI , OrderDetailAPI , CreateOrderAPI , ApplyCouponAPI 



app_name = 'orders'

urlpatterns = [
    path('', OrderList.as_view()),
    path('checkout',checkout),
    path('add_to_cart', add_to_cart ,name ='add_to_cart'),
    path('<int:id>/remove-from-cart',remove_from_cart),
    path('order-summary/', order_summary, name='order_summary'),
    #mpesa integrations
    path('mpesa_payment/<int:order_id>/', mpesa_initiate_payment, name='mpesa_payment'),
    path('mpesa_payment_success/', mpesa_payment_success, name='mpesa_payment_success'),
    path('mpesa_payment_failed/', mpesa_payment_failed, name='mpesa_payment_failed'),


    # api  
    path('api/list/<str:username>',OrderListAPI.as_view()),
    path('api/list/<str:username>/create-order',CreateOrderAPI.as_view()),
    path('api/<str:username>/cart', CartDetailCreateAPI.as_view()),
    path('api/<str:username>/cart/apply-coupon', ApplyCouponAPI.as_view()),
    path('api/list/<str:username>/<int:pk>',OrderDetailAPI.as_view()),
]
