from .models import Item, Drinks, Food
from rest_framework import serializers

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class DrinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drinks
        fields = '__all__'

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'