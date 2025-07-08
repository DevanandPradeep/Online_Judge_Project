from django.shortcuts import render
from executor.models import UserSolvedProblem  # ✅ import this
from .models import Problem

def problem_list_html(request):
    user = request.user
    problems = Problem.objects.all()

    # Get set of problem IDs solved by this user
    solved_problems = set(
        UserSolvedProblem.objects.filter(user=user).values_list('problem_id', flat=True)
    )

    # Add is_solved attribute to each problem
    for problem in problems:
        problem.is_solved = problem.id in solved_problems

    return render(request, 'problems/problem_list.html', {'problems': problems})
