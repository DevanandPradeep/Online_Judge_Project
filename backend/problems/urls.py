from django.urls import path
from . import views

urlpatterns = [
    path('', views.problem_list, name='problem_list'),
    path('<int:pk>/', views.problem_detail, name='problem_detail'),
    path('create/', views.problem_create, name='problem_create'),
    path('<int:pk>/edit/', views.problem_update, name='problem_update'),
    path('<int:pk>/delete/', views.problem_delete, name='problem_delete'),
]
