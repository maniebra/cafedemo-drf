from django.urls import path, include
from .views import *

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('order/', OrderView.as_view(), name='order'),
    path('order/<int:id>/', OrderItemsView.as_view(), name='order_items'),
]