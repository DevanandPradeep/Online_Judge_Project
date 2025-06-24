from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

urlpatterns = [
    path('', lambda request: JsonResponse({"message": "Welcome to Online Judge API"})),
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),
]

