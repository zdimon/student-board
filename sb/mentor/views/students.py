from django.shortcuts import render
from django.contrib.auth import login
from django.shortcuts import redirect
from mentor.models import Mentor, Mentor2Course, Mentor2Student
from course.models import Course

def students(request):
    students = Mentor2Student.objects.filter(mentor=request.user.mentor)
    return render(request,'mentor/students.html',{"students": students})
