from django.shortcuts import render
from student.models import Student
from student.forms.student import StudentForm
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib import messages

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
        login(request, s)
        messages.info(request, 'You have been successfuly registrated.')
        return redirect('student-cabinet')
    return render(request,'student/registration.html')

