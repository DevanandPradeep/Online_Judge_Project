import subprocess
import os
from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CodeExecutionSerializer
from django.shortcuts import render
from .forms import CodeExecutionForm
from problems.models import Problem  # Import Problem
from .models import Submission, UserSolvedProblem
from django.contrib.auth.decorators import login_required
from .ai_helpers import generate_hint
from django.http import JsonResponse
import openai
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI
from decouple import config
from django.conf import settings

class CodeExecutorView(APIView):
    def post(self, request):
        serializer = CodeExecutionSerializer(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data['code']
            with open("temp.py", "w") as f:
                f.write(code)
            try:
                output = subprocess.check_output(["python3", "temp.py"], stderr=subprocess.STDOUT, timeout=5)
                return Response({"output": output.decode()}, status=status.HTTP_200_OK)
            except subprocess.CalledProcessError as e:
                return Response({"error": e.output.decode()}, status=status.HTTP_400_BAD_REQUEST)
            except subprocess.TimeoutExpired:
                return Response({"error": "Code execution timed out"}, status=status.HTTP_408_REQUEST_TIMEOUT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@login_required
def code_executor_form_view(request):
    run_output = ""
    verdict = ""
    hidden_results = []
    problem = None

    problem_id = request.GET.get('problem_id')
    if problem_id:
        problem = get_object_or_404(Problem, pk=problem_id)

    if request.method == "POST":
        form = CodeExecutionForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            language = form.cleaned_data['language']
            custom_input = form.cleaned_data['custom_input'] or ""
            filename = "temp.py" if language == 'python' else "temp.c" if language == 'c' else "temp.cpp"

            with open(filename, "w") as f:
                f.write(code)

            action = request.POST.get('action')

            if action == 'run':
                try:
                    if language == 'python':
                        result = subprocess.run(["python3", filename], input=custom_input.encode(), capture_output=True, timeout=5)
                    elif language == 'c':
                        subprocess.run(["gcc", filename, "-o", "temp_c_exe"], check=True)
                        result = subprocess.run(["./temp_c_exe"], input=custom_input.encode(), capture_output=True, timeout=5)
                    elif language == 'cpp':
                        subprocess.run(["g++", filename, "-o", "temp_cpp_exe"], check=True)
                        result = subprocess.run(["./temp_cpp_exe"], input=custom_input.encode(), capture_output=True, timeout=5)

                    stdout = result.stdout.decode().strip()
                    stderr = result.stderr.decode().strip()
                    run_output = stdout if stdout else stderr or "No Output"
                except Exception as e:
                    run_output = f"❌ Error: {str(e)}"

            elif action == 'submit' and problem:
                try:
                    all_passed = True
                    hidden_test_results = []

                    for case in problem.hidden_test_cases:
                        h_input = case['input']
                        h_expected = case['output']

                        result = subprocess.run(["python3", filename], input=h_input.encode(), capture_output=True, timeout=5)
                        h_actual = result.stdout.decode().strip()
                        passed = (h_actual == h_expected)

                        hidden_test_results.append({
                            'input': h_input,
                            'expected': h_expected,
                            'actual': h_actual,
                            'result': 'Pass' if passed else 'Fail'
                        })

                        if not passed:
                            all_passed = False

                    verdict = "✅ Passed All Hidden Cases" if all_passed else "❌ Some Hidden Cases Failed"
                    hidden_results = hidden_test_results

                    if request.user.is_authenticated:
                        # Save submission
                        Submission.objects.create(
                            user=request.user,
                            problem=problem,
                            code=code,
                            language=language,
                            verdict=verdict
                        )

                        # ✅ Save solve if passed and not already done
                        if all_passed:
                            already_solved = UserSolvedProblem.objects.filter(user=request.user, problem=problem).exists()
                            if not already_solved:
                                UserSolvedProblem.objects.create(user=request.user, problem=problem)

                                # ✅ Increment problem count
                                request.user.problems_solved += 1
                                request.user.save()

                except Exception as e:
                    verdict = f"❌ Error: {str(e)}"

    else:
        form = CodeExecutionForm()

    return render(request, 'executor/code_form.html', {
        'form': form,
        'run_output': run_output,
        'verdict': verdict,
        'hidden_results': hidden_results,
        'problem': problem,
    })

@login_required
def problem_submissions_view(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    submissions = Submission.objects.filter(user=request.user, problem=problem).order_by('-created_at')
    already_done = UserSolvedProblem.objects.filter(user=request.user, problem=problem).exists()

    return render(request, 'executor/problem_submissions.html', {
        'problem': problem,
        'submissions': submissions,
        'already_done': already_done,
    })

@csrf_exempt
@login_required
def generate_hint_view(request, problem_id):
    try:
        problem = Problem.objects.get(pk=problem_id)
        prompt = f"Give a short and helpful programming hint for this problem:\n\n{problem.title}\n{problem.description}"
        hint = generate_hint(prompt)
        return JsonResponse({"hint": hint})
    except Exception as e:
        return JsonResponse({"hint": f"⚠️ Failed to generate hint:\n{str(e)}"}, status=500)