from xml import dom
from django.shortcuts import render
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib import messages
from student.models import Course
from course.models import Lesson
from mentor.models import Mentor2Course

def course_detail(request, course_id):
    course = Course.objects.get(pk=course_id)
    lessons = Lesson.objects.filter(course=course).order_by('number')
    return render(request,'mentor/course_detail.html',{"course": course, "lessons": lessons})
