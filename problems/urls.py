from django.urls import path
from .views import problem_list_html, problem_detail_html

urlpatterns = [
    path('', problem_list_html, name='problem_list_html'),
    path('<int:pk>/', problem_detail_html, name='problem_detail_html'),
]
