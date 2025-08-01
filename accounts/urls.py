# accounts/urls.py

from django.urls import path
from .views import register_view, login_view, logout_view, user_view
from .views import leaderboard_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('user/', user_view, name='user-profile'),
    path('leaderboard/', leaderboard_view, name='leaderboard'),
]
