from django.forms import ModelForm
from student.models import Student2Lab
from django import forms

class Student2LabForm(ModelForm):
    class Meta:
        model = Student2Lab
        fields = [ 'gitlink', 'file']