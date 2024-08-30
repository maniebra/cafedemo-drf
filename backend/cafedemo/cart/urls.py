from django.urls import path, include
from .views import *

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/<int:id>', CartParamsView.as_view(), name='cart-params'),
    path('order/', OrderView.as_view(), name='order'),
    path('order/<int:id>', OrderParamsView.as_view(), name='order-params'),
    path('order-items/<int:id>/', OrderItemsView.as_view(), name='order_items'),
]