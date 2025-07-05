from django.shortcuts import render, get_object_or_404
from .models import Problem

# List all problems in HTML
def problem_list_html(request):
    problems = Problem.objects.all()
    return render(request, 'problems/problem_list.html', {'problems': problems})

# View problem detail in HTML
def problem_detail_html(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    return render(request, 'problems/problem_detail.html', {'problem': problem})
