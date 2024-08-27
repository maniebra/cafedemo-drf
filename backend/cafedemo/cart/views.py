from django.shortcuts import render
from drf_spectacular.utils import extend_schema_serializer, extend_schema, OpenApiExample
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from backend.cafedemo.users.utils import is_current_user_admin
from rest_framework.permissions import IsAuthenticated, AllowAny
