from django.urls import path
from .views import problem_list_html

urlpatterns = [
    path('', problem_list_html, name='problem_list_html'),
]
