from xml import dom
from django.shortcuts import render
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib import messages
from student.models import Course
from mentor.models import Mentor2Course

def courses(request):
    courses = Mentor2Course.objects.filter(user=request.user.mentor)
    return render(request,'mentor/courses.html',{"courses": courses})
