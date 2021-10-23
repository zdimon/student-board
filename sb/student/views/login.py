from django.shortcuts import render
from student.models import Student, StudentGroup
from student.forms.student import StudentForm
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.info(request, _('Добро пожаловать на сайт.'))   
            return redirect('/')         
        else:
            messages.info(request, _('Ошибка. Неправильный логин или пароль'))            
    return render(request,'student/login.html',{})

