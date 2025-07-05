from django.db import models

class Problem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    difficulty = models.CharField(max_length=20)

    def __str__(self):
        return self.title
