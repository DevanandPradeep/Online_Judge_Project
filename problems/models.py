from django.db import models

class Problem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    sample_input = models.TextField()
    sample_output = models.TextField()
    hidden_test_cases = models.JSONField(default=list)
    constraints = models.TextField(blank=True, null=True)  # Automatically adds current timestamp

    def __str__(self):
        return self.title
