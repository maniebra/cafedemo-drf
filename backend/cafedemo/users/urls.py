from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .auth_utils import UserTokenObtainPairView
from backend.cafedemo.users.views import UsersNoParamViewSet, TokenTestView, UsersParamsViewSet

router = DefaultRouter()

urlpatterns = [
    path('', UsersNoParamViewSet.as_view(), name='users_no_param'),
    path('<int:id>', UsersParamsViewSet.as_view(), name='users_param'),
    path('auth/token/', UserTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/test/', TokenTestView.as_view(), name='token_test')
]