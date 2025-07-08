import subprocess
import os
import time
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
from django.contrib.auth import get_user_model
User = get_user_model()


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
            custom_input = form.cleaned_data['custom_input']

            filename = "temp.py" if language == 'python' else "temp.c" if language == 'c' else "temp.cpp"

            with open(filename, "w") as f:
                f.write(code)

            action = request.POST.get('action')

            # ➔ Normalize custom input: handle both '1 2' and '1\n2'
            if custom_input and ' ' in custom_input:
                custom_input = custom_input.replace(' ', '\n')

            # ➔ If Run button pressed:
            if action == 'run':
                if not custom_input.strip():
                    run_output = "⚠️ No custom input provided."
                else:
                    try:
                        start = time.time()
                        if language == 'python':
                            result = subprocess.run(["python3", filename], input=custom_input.encode(), capture_output=True, timeout=5)
                        elif language == 'c':
                            subprocess.run(["gcc", filename, "-o", "temp_c_exe"], check=True)
                            result = subprocess.run(["./temp_c_exe"], input=custom_input.encode(), capture_output=True, timeout=5)
                        elif language == 'cpp':
                            subprocess.run(["g++", filename, "-o", "temp_cpp_exe"], check=True)
                            result = subprocess.run(["./temp_cpp_exe"], input=custom_input.encode(), capture_output=True, timeout=5)

                        exec_time = time.time() - start
                        stdout = result.stdout.decode().strip()
                        stderr = result.stderr.decode().strip()

                        if exec_time > 4.8:
                            run_output = "⏱️ Time Limit Exceeded (TLE)"
                        else:
                            run_output = stdout if stdout else stderr or "No Output"

                    except subprocess.TimeoutExpired:
                        run_output = "⏱️ Time Limit Exceeded (TLE)"
                    except Exception as e:
                        run_output = f"❌ Error: {str(e)}"

            # ➔ If Submit button pressed:
            elif action == 'submit' and problem:
                try:
                    all_passed = True
                    hidden_test_results = []

                    for case in problem.hidden_test_cases:
                        h_input = case['input']
                        h_expected = case['output']

                        # Normalize hidden test case inputs too
                        if ' ' in h_input:
                            h_input = h_input.replace(' ', '\n')

                        try:
                            result = subprocess.run(["python3", filename], input=h_input.encode(), capture_output=True, timeout=5)
                            h_actual = result.stdout.decode().strip()
                            passed = (h_actual == h_expected)

                        except subprocess.TimeoutExpired:
                            h_actual = "Time Limit Exceeded"
                            passed = False

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
                        Submission.objects.create(
                            user=request.user,
                            problem=problem,
                            code=code,
                            language=language,
                            verdict=verdict
                        )

                        if all_passed:
                            already_solved = UserSolvedProblem.objects.filter(user=request.user, problem=problem).exists()
                            if not already_solved:
                                UserSolvedProblem.objects.create(user=request.user, problem=problem)

                                # ✅ Refresh the user object from the database
                                user = User.objects.get(pk=request.user.pk)
                                user.problems_solved = UserSolvedProblem.objects.filter(user=user).count()  # Safer: recalculate
                                user.save()

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