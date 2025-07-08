from django.urls import path
from .views import CodeExecutorView, code_executor_form_view
from . import views
from .views import generate_hint_view

urlpatterns = [
    path('hint/<int:problem_id>/', generate_hint_view, name='generate_hint'),
    path('run/', CodeExecutorView.as_view(), name='code-executor'),
    path('run/form/', code_executor_form_view, name='html-code-run'),
    path('run/<int:problem_id>/', code_executor_form_view, name='executor_view'),  # NEW: supports problem id
    path('submissions/<int:problem_id>/', views.problem_submissions_view, name='problem_submissions'),
]
