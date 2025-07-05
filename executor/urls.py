from django.urls import path
from .views import CodeExecutorView, code_executor_form_view
from . import views

urlpatterns = [
    path('run/', CodeExecutorView.as_view(), name='code-executor'),
    path('run/form/', code_executor_form_view, name='html-code-run'),
    path('run/<int:problem_id>/', code_executor_form_view, name='executor_view'),  # NEW: supports problem id
    path('submissions/<int:problem_id>/', views.problem_submissions_view, name='problem_submissions'),
]
