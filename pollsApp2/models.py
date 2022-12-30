from django.db import models

class Question(models.Model):
    question = models.TextField()
    created_by = models.TextField()

class Choices(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.TextField()
    count = models.IntegerField(default=0)
