# backend/cafedemo/users/auth_utils.py

import logging
from rest_framework import serializers
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.backends import BaseBackend
from backend.cafedemo.users.models import User

logger = logging.getLogger(__name__)

class EmailBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=email)
            logger.debug(f"User found: {user.email}")
        except User.DoesNotExist:
            logger.error(f"User not found with email: {email}")
            return None

        if user.check_password(password):
            logger.debug(f"Password check passed for user: {user.email}")
            return user
        logger.error(f"Password check failed for user: {user.email}")
        return None

    def get_user(self, id):
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist:
            return None

class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = User.objects.filter(email=email).first()

        if user is None:
            logger.error(f"No active account found with the given credentials: {email}")
            raise serializers.ValidationError("No active account found with the given credentials")

        if not user.check_password(password):
            logger.error(f"Password check failed for user: {email}")
            raise serializers.ValidationError("No active account found with the given credentials")

        attrs['username'] = user.email
        attrs['user_id'] = user.id

        return super().validate(attrs)

@permission_classes([AllowAny])
class UserTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer