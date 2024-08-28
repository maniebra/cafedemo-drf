from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    path('users/', include("users.urls"), name='users'),
    path('menu/', include("menu.urls"), name='menu'),
    path('cart/', include("cart.urls"), name='cart'),
    path('apidoc/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('apidoc/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('apidoc/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
