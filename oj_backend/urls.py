from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.urls import path, include
from .views import dashboard_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('accounts.urls')),
    path('problems/', include('problems.urls')),
    path("executor/", include("executor.urls")),
]

