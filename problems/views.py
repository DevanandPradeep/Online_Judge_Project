from django.shortcuts import render, get_object_or_404
from .models import Problem

# List all problems in HTML
def problem_list_html(request):
    problems = Problem.objects.all()
    return render(request, 'problems/problem_list.html', {'problems': problems})

