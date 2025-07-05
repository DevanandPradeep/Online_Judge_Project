from django.urls import path
from .views import (
    SubmissionListView,
    SubmissionDetailView,
    SubmissionCreateView,
    SubmissionUpdateView,
    SubmissionDeleteView
)

urlpatterns = [
    path('', SubmissionListView.as_view(), name='submission_list'),
    path('<int:pk>/', SubmissionDetailView.as_view(), name='submission_detail'),
    path('create/', SubmissionCreateView.as_view(), name='submission_create'),
    path('<int:pk>/update/', SubmissionUpdateView.as_view(), name='submission_update'),
    path('<int:pk>/delete/', SubmissionDeleteView.as_view(), name='submission_delete'),
]
