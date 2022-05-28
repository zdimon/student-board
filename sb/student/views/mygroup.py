from django.shortcuts import render
from course.models import Course
from django.contrib import messages
from student.models import Student2Course, Student2Lab, Student
from course.models import Lab
from django.shortcuts import redirect


def mygroup(request):
    students = Student.objects.filter(group=request.user.student.group)
    return render(request,'student/mygroup.html', {"students": students})

