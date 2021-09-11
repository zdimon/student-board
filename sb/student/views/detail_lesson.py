from django.shortcuts import render
from course.models import Course, Lesson, Topic
from django.contrib import messages
from student.models import Student2Course
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect


def detail_lesson(request, lesson_id):
    lesson = Lesson.objects.get(pk=lesson_id)
    topics = Topic.objects.filter(lesson=lesson)
    return render(request,'student/detail_lesson.html', {"lesson": lesson, "topics": topics})
