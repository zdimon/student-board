from django.shortcuts import render
from student.models import Student
from student.forms.student import StudentForm
from django.contrib.auth import login
from django.shortcuts import redirect

def profile(request):
    form = StudentForm(instance=request.user.student)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=request.user.student)
        if form.is_valid():
            form.save()

    return render(request,'student/profile.html', {"form": form})
