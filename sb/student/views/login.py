from django.shortcuts import render
from student.models import Student, StudentGroup
from student.forms.student import StudentForm
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _


def login(request):
    if request.method == 'POST':
        pass
    return render(request,'student/login.html',{})

