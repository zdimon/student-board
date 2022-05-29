from django.shortcuts import render
from mentor.models import Invitation
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse
from student.models import Student
from course.models import Lesson
import random
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.utils.translation import ugettext as _


def newlesson(request, uuid, lesson_id):
    student = Student.objects.get(uuid=uuid)
    lesson = Lesson.objects.get(pk=lesson_id)
    login(request, student)
    return redirect(reverse('detail-lesson-student', kwargs={'lesson_id':lesson.pk}))
    