from django.shortcuts import render
from django.contrib.auth import login
from student.models import Student
from django.shortcuts import redirect
from django.urls import reverse


def paid_course(request, uuid, course_id):
    user = Student.objects.get(uuid=uuid)
    login(request, user)
    return redirect(reverse('detail-course-student', kwargs={"course_id": course_id}))


def paid_lesson(request, uuid, lesson_id):
    user = Student.objects.get(uuid=uuid)
    login(request, user)
    return redirect(reverse('detail-lesson-student', kwargs={"lesson_id": lesson_id}))