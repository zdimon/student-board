from django.shortcuts import render
from django.contrib.auth import login
from django.shortcuts import redirect
from mentor.models import Mentor, Mentor2Course
from course.models import Course

def students(request):
    
    return render(request,'mentor/students.html',{})
