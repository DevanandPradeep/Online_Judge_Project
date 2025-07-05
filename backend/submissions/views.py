from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Submission

class SubmissionListView(ListView):
    model = Submission
    template_name = 'submissions/submission_list.html'

class SubmissionDetailView(DetailView):
    model = Submission
    template_name = 'submissions/submission_detail.html'

class SubmissionCreateView(CreateView):
    model = Submission
    fields = ['problem', 'code', 'language']
    template_name = 'submissions/submission_form.html'
    success_url = reverse_lazy('submission_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class SubmissionUpdateView(UpdateView):
    model = Submission
    fields = ['code', 'language']
    template_name = 'submissions/submission_form.html'
    success_url = reverse_lazy('submission_list')

class SubmissionDeleteView(DeleteView):
    model = Submission
    template_name = 'submissions/submission_confirm_delete.html'
    success_url = reverse_lazy('submission_list')
