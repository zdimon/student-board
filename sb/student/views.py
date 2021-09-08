from django.shortcuts import render
from .models import Student

def registration(request):
    if request.method == 'POST':
        s = Student()
        s.fname = request.POST['first_name']
        s.lname = request.POST['last_name']
        s.username = request.POST['email']
        s.account = 0
        s.set_password(request.POST['password'])
        s.email = request.POST['email']
        s.is_active = True
        s.save()
        print(request.POST['first_name'])
    return render(request,'student/registration.html')
