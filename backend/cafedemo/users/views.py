# backend/cafedemo/users/views.py

import logging

from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from .models import User
from .serializers import UserSerializer, UserCreateSerializer
from .utils import get_current_user, is_current_user_admin

logger = logging.getLogger(__name__)


class UsersNoParamViewSet(APIView):
    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [AllowAny]

    @extend_schema(
        request=None,
        responses={201: UserSerializer, 401: OpenApiExample('Authorization Error')},
        description="Get the current user's information or all users if the current user is an admin",
    )
    def get(self, request):
        self.permission_classes = [IsAuthenticated]
        self.check_permissions(request)
        current_user = get_current_user(request)
        if is_current_user_admin(request):
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        return Response(status=201, data=UserSerializer(current_user).data)

    @extend_schema(
        request=UserCreateSerializer,
        responses={201: UserSerializer, 400: OpenApiExample('Validation Error', value={"error": "Invalid data"})},
        description="Create a new user",
    )
    def post(self, request):
        self.permission_classes = [AllowAny]
        self.check_permissions(request)
        user_data = request.data
        if 'is_admin' in user_data:
            return Response(status=403, data={"message": "You cannot create an admin user."})
        serializer = UserSerializer(data=user_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=400, data=serializer.errors)

    @extend_schema(
        request=None,
        responses={201: UserSerializer, 401: OpenApiExample('Authorization Error')},
        description="Delete the current user",
    )
    def delete(self, request):
        self.permission_classes = [IsAuthenticated]
        self.check_permissions(request)
        user = User.objects.filter(id=id).first()
        if user:
            user.delete()
            return Response(status=204)
        return Response(status=404)



class UsersParamsViewSet(APIView):
    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=None,
        responses={200: UserSerializer, 401: OpenApiExample('Authorization Error'),
                   403: OpenApiExample('Permission Error')},
        description="Get a specific user's information",
    )
    def get(self, request, id):
        if is_current_user_admin(request):
            user = User.objects.filter(id=id).first()
            if user:
                serializer = UserSerializer(user)
                return Response(serializer.data)
            return Response(status=404)
        return Response(status=403, data={"message": "You do not have permission to view this user."})

    @extend_schema(
        request=UserCreateSerializer,
        responses={200: UserSerializer, 400: OpenApiExample('Validation Error', value={"error": "Invalid data"}),
                   401: OpenApiExample('Authorization Error'), 403: OpenApiExample('Permission Error'),
                   404: OpenApiExample('Not Found')},
        description="Update a specific user's information",
    )
    def put(self, request, id):
        user = User.objects.filter(id=id).first()
        if user:
            if is_current_user_admin(request) or user.id == request.user.id:
                if 'is_admin' in request.data and not is_current_user_admin(request):
                    return Response(status=403, data={"message": "You cannot set is_admin if you are not an admin."})
                user_data = request.data
                serializer = UserSerializer(user, data=user_data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(status=400, data=serializer.errors)
            return Response(status=403, data={"message": "You do not have permission to update this user."})
        return Response(status=404)

    @extend_schema(
        request=None,
        responses={204: OpenApiExample('No Content'), 401: OpenApiExample('Authorization Error'),
                   403: OpenApiExample('Permission Error'), 404: OpenApiExample('Not Found')},
        description="Delete a specific user",
    )
    def delete(self, request, id):
        user = User.objects.filter(id=id).first()
        if user:
            if is_current_user_admin(request):
                user.delete()
                return Response(status=204)
            return Response(status=403, data={"message": "You do not have permission to delete this user."})
        return Response(status=404)

class TokenTestView(APIView):
    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logger.debug(f"Authenticated user: {request.user}")
        return Response({"user_id": request.user.id})