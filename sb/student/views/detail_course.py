from django.shortcuts import render
from course.models import Course, Lesson
from django.contrib import messages
from student.models import Student2Course
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect


def detail_course(request, course_id):
    course = Course.objects.get(pk=course_id)
    lessons = Lesson.objects.filter(course=course).order_by('number')
    return render(request,'student/detail_course.html', {"course": course, "lessons": lessons})
