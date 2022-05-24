from django.forms import ModelForm
from student.models import Student2ExamAnswer
from django import forms

class Student2ExamAnswerForm(ModelForm):
    class Meta:
        model = Student2ExamAnswer
        fields = [ 'answer', 'user', 'exam']
        widgets = {'user': forms.HiddenInput(), 'exam': forms.HiddenInput()}