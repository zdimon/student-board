from django.shortcuts import render
from course.models import Course, Lesson
from student.models import Student2Course, StudentPayment, StudentGroup
from django.shortcuts import redirect
from student.models import Student
from django.contrib.auth import login
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _


def prepay(request,course_id, lesson_id):
    groups = StudentGroup.objects.all().order_by('name')
    course = Course.objects.get(pk=course_id)
    lesson = Lesson.objects.get(pk=lesson_id)
    if request.method == "POST":
        pass
    return render(request, 'dash/prepay.html', {"groups": groups, "lesson": lesson, "course": course})
