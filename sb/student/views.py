from django.shortcuts import render
from .models import Student

def registration(request):
    if request.method == 'POST':
        s = Student()
        s.first_name = request.POST['first_name']
        s.last_name = request.POST['last_name']
        s.account = 0
        s.save()
        print(request.POST['first_name'])
    return render(request,'student/registration.html')
