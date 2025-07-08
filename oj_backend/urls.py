from django.contrib import admin
from django.urls import path, include
from .views import dashboard_view
from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'index.html')


@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')

urlpatterns = [
    path('', home, name='home'), 
    path('dashboard/', dashboard_view, name='dashboard'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  
    path('problems/', include('problems.urls')),
    path('executor/', include('executor.urls')),
]
