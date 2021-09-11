from django.shortcuts import render
from course.models import Course
from django.contrib import messages
from student.models import Student2Course

def labs(request):
   
    return render(request,'student/labs.html', {})
