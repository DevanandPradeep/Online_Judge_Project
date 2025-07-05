from django.db import models

class Problem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    sample_input = models.TextField(blank=True, null=True)
    sample_output = models.TextField(blank=True, null=True)
    hidden_test_cases = models.JSONField(default=list, blank=True, null=True)  # For hidden test cases
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically adds current timestamp

    def __str__(self):
        return self.title
