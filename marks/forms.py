
from django import forms
from .models import Student, MarkField

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["name"]

class MarkFieldForm(forms.ModelForm):
    class Meta:
        model = MarkField
        fields = ["name"]
