from django.db import models
from django.conf import settings
from problems.models import Problem

class Submission(models.Model):
    LANGUAGE_CHOICES = [
        ('python', 'Python'),
        ('cpp', 'C++'),
        ('java', 'Java'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    code = models.TextField()
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES)
    result = models.CharField(max_length=100, default='Pending')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.problem.title} - {self.result}"
