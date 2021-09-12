from django.shortcuts import render
from django.contrib.auth import login
from django.shortcuts import redirect
from mentor.models import Mentor, Mentor2Course
from course.models import Course

def cabinet(request):
    joined_courses = []
    courses = Course.objects.all()
    for c in Mentor2Course.objects.filter(user=request.user.mentor):
        joined_courses.append(c.course.pk)
    return render(request,'mentor/cabinet.html',{"courses": courses, "joined_courses": joined_courses})
