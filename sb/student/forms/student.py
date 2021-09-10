from django.forms import ModelForm
from student.models import Student
from django import forms

class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = [ 'fname', 'lname', 'surname', 'image', 'group']