from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import login as l
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                l(request, user)   
                messages.info(request, _('You was joined to this course.'))
        else:
            print('Error data!')  
            messages.warning(request, _('Wrong email or password!'))  


    return redirect('/')
