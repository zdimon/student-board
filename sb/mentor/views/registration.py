from django.shortcuts import render
from django.contrib.auth import login
from django.shortcuts import redirect
from mentor.models import Mentor


def registration(request):
    if request.method == 'POST':
        s = Mentor()
        s.fname = request.POST['first_name']
        s.lname = request.POST['last_name']
        s.surname = request.POST['surname']
        s.username = request.POST['email']
        s.set_password(request.POST['password'])
        s.email = request.POST['email']
        s.is_active = True
        s.save()
        login(request, s)
        return redirect('mentor-cabinet')
    return render(request,'mentor/registration.html')
