from django.shortcuts import render, get_object_or_404, redirect
from .models import Problem
from .forms import ProblemForm  # you'll create this form

def problem_list(request):
    problems = Problem.objects.all()
    return render(request, 'problems/problem_list.html', {'problems': problems})

def problem_detail(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    return render(request, 'problems/problem_detail.html', {'problem': problem})

def problem_create(request):
    if request.method == "POST":
        form = ProblemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('problem_list')
    else:
        form = ProblemForm()
    return render(request, 'problems/problem_form.html', {'form': form})

def problem_update(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    form = ProblemForm(request.POST or None, instance=problem)
    if form.is_valid():
        form.save()
        return redirect('problem_list')
    return render(request, 'problems/problem_form.html', {'form': form})

def problem_delete(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    if request.method == "POST":
        problem.delete()
        return redirect('problem_list')
    return render(request, 'problems/problem_confirm_delete.html', {'problem': problem})
