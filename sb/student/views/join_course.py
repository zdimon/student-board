from django.shortcuts import render
from course.models import Course
from django.contrib import messages
from student.models import Student2Course
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect


def join_course(request, course_id):
    course = Course.objects.get(pk=course_id)
    u2c = Student2Course.objects.create(
        user = request.user.student,
        course = course
    )
    messages.info(request, _('You was joined to this course.'))
    return redirect('student-cabinet')
