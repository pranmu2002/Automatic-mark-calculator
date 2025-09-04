
from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    def __str__(self): return self.name

class MarkField(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    def __str__(self): return self.name

class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    field = models.ForeignKey(MarkField, on_delete=models.CASCADE)
    score = models.FloatField(default=0)
    def __str__(self): return f"{self.student.name} - {self.field.name}: {self.score}"
