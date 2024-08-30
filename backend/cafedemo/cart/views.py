from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from backend.cafedemo.users.utils import is_current_user_admin
from backend.cafedemo.users.models import User
from backend.cafedemo.cart.models import *
from backend.cafedemo.cart.serializers import CartSerializer, OrderSerializer, OrderItemsSerializer

# Create your views here.

class CartView(APIView):
    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=CartSerializer,
        responses={200: CartSerializer}
    )
    def post(self, request):
        data = request.data
        data['user'] = request.user.id
        serializer = CartSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={200: CartSerializer(many=True)}
    )
    def get(self, request):
        user = User.objects.get(id=request.user.id)
        queryset = Cart.objects.filter(user=user)
        serializer = CartSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartParamsView(APIView):
    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: CartSerializer}
    )
    def put(self, request, id):
        data = request.data
        user = User.objects.get(id=request.user.id)
        cart = Cart.objects.get(user=user, product=data['product'])
        serializer = CartSerializer(cart, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={200: CartSerializer}
    )
    def delete(self, request, id):
        user = User.objects.get(id=request.user.id)
        cart = Cart.objects.get(user=user, product=id)
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderView(APIView):
    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: OrderSerializer}
    )
    def post(self, request):
        user = User.objects.get(id=request.user.id)
        total = 0
        cart_items = Cart.objects.filter(user=user)
        for item in cart_items:
            total += item.get_total()
        order = Order.objects.create(user=user, total=total)
        for item in cart_items:
            OrderItems.objects.create(order=order, product=item.product, quantity=item.quantity)
            item.delete()
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        responses={200: OrderSerializer(many=True)}
    )
    def get(self, request):
        queryset = Order.objects.all()
        if not is_current_user_admin(request):
            user = User.objects.get(id=request.user.id)
            queryset = Order.objects.filter(user=user)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderParamsView(APIView):
    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]


    @extend_schema(
        responses={200: OrderSerializer(many=True)}
    )
    def get(self, request, id):
        if is_current_user_admin(request):
            queryset = Order.objects.filter(id=id)
            serializer = OrderSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)

    @extend_schema(
        responses={200: OrderSerializer}
    )
    def put(self, request, id):
        if is_current_user_admin(request):
            order = Order.objects.get(id)
            data = request.data
            serializer = OrderSerializer(order, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)

    @extend_schema(
        responses={200: OrderSerializer}
    )
    def delete(self, request, id):
        if is_current_user_admin(request):
            order = Order.objects.get(id)
            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class OrderItemsView(APIView):
    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: OrderItemsSerializer}
    )
    def get(self, request, id):
        user = User.objects.get(id=request.user.id)
        order = Order.objects.get(id=id)
        if order.user != user and not is_current_user_admin(request.user):
            return Response(status=status.HTTP_403_FORBIDDEN)
        queryset = OrderItems.objects.filter(order=order)
        serializer = OrderItemsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={200: OrderItemsSerializer}
    )
    def put(self, request, id):
        if is_current_user_admin(request.user):
            data = request.data
            order = Order.objects.get(id=id)
            order_item = OrderItems.objects.get(order=order, product=data['product'])
            serializer = OrderItemsSerializer(order_item, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)

    @extend_schema(
        responses={200: OrderItemsSerializer}
    )
    def delete(self, request, id):
        if is_current_user_admin(request.user):
            data = request.data
            order = Order.objects.get(id=id)
            order_item = OrderItems.objects.get(order=order, product=data['product'])
            order_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)