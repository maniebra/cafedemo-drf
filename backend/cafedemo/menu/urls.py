from django.urls import path, include
from .views import *

urlpatterns = [
    path('drinks/', DrinksNoParamViewSet.as_view(), name='drinks_no_param'),
    path('drinks/<int:id>', DrinksParamViewSet.as_view(), name='drinks_param'),
    path('food/', FoodNoParamViewSet.as_view(), name='food_no_param'),
    path('food/<int:id>', FoodParamViewSet.as_view(), name='food_param'),
    path('item/', ItemNoParamViewSet.as_view(), name='item_no_param'),
]