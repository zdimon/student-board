from django.shortcuts import render
from course.models import Course
from django.contrib import messages
from student.models import Student2Course
from course.models import Lab



def labs(request):
    courses = []
    tmp = Student2Course.objects.filter(user=request.user.student)
    for c in tmp:
        courses.append(c.course)
    return render(request,'student/labs.html', {"courses": courses})
