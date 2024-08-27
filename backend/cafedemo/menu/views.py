from django.shortcuts import render
from drf_spectacular.utils import extend_schema_serializer, extend_schema, OpenApiExample
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from .models import Item, Drinks, Food
from .serializers import ItemSerializer, DrinksSerializer, FoodSerializer
from backend.cafedemo.users.utils import is_current_user_admin
from rest_framework.permissions import IsAuthenticated, AllowAny


class DrinksNoParamViewSet(APIView):
    authentication_classes = [JWTTokenUserAuthentication]

    permission_classes = [AllowAny]

    @extend_schema(
        request=None,
        responses={200: DrinksSerializer}
    )
    def get(self, request):
        self.permission_classes = [AllowAny]
        self.check_permissions(request)
        drinks = Drinks.objects.all()
        serializer = DrinksSerializer(drinks, many=True)
        return Response(serializer.data)


    @extend_schema(
        request=DrinksSerializer,
        responses = {200: DrinksSerializer, 401: OpenApiExample('Authorization Error'),
                 403: OpenApiExample('Permission Error')},
    )
    def post(self, request):
        self.permission_classes = [IsAuthenticated]
        self.check_permissions(request)
        if not is_current_user_admin(request):
            return Response({"error": "You are not authorized to perform this action"},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = DrinksSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DrinksParamViewSet(APIView):
    authentication_classes = [JWTTokenUserAuthentication]

    permission_classes = [AllowAny]
    @extend_schema(
        request=DrinksSerializer,
        responses=DrinksSerializer
    )
    def get(self, request, id):
        try:
            drink = Drinks.objects.get(id=id)
        except Drinks.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = DrinksSerializer(drink)
        return Response(serializer.data)

    @extend_schema(
        request=DrinksSerializer,
        responses=DrinksSerializer
    )
    def put(self, request, id):
        try:
            drink = Drinks.objects.get(id=id)
        except Drinks.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = DrinksSerializer(drink, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=None,
        responses=None
    )
    def delete(self, request, id):
        try:
            drink = Drinks.objects.get(id=id)
        except Drinks.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        drink.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class FoodNoParamViewSet(APIView):
    authentication_classes = [JWTTokenUserAuthentication]

    permission_classes = [AllowAny]
    @extend_schema(
        request=None,
        responses=FoodSerializer
    )
    def get(self, request):
        self.permission_classes = [AllowAny]
        self.check_permissions(request)
        food = Food.objects.all()
        serializer = FoodSerializer(food, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=FoodSerializer,
        responses=FoodSerializer
    )
    def post(self, request):
        self.permission_classes = [IsAuthenticated]
        self.check_permissions(request)
        if not is_current_user_admin(request):
            return Response({"error": "You are not authorized to perform this action"},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = FoodSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FoodParamViewSet(APIView):
    authentication_classes = [JWTTokenUserAuthentication]

    permission_classes = [AllowAny]
    @extend_schema(
        request=FoodSerializer,
        responses=FoodSerializer
    )
    def get(self, request, id):
        try:
            food = Food.objects.get(id=id)
        except Food.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = FoodSerializer(food)
        return Response(serializer.data)

    @extend_schema(
        request=FoodSerializer,
        responses=FoodSerializer
    )
    def put(self, request, id):
        try:
            food = Food.objects.get(id=id)
        except Food.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = FoodSerializer(food, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=None,
        responses=None
    )
    def delete(self, request, id):
        try:
            food = Food.objects.get(id=id)
        except Food.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        food.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ItemNoParamViewSet(APIView):
    authentication_classes = [JWTTokenUserAuthentication]

    permission_classes = [AllowAny]
    @extend_schema(
        request=None,
        responses=ItemSerializer
    )
    def get(self, request):
        self.permission_classes = [AllowAny]
        self.check_permissions(request)
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)
