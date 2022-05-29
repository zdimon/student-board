from django.shortcuts import render
from course.models import Course
from django.contrib import messages
from mentor.models import Mentor2Course
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect


def join_course(request, course_id):
    course = Course.objects.get(pk=course_id)
    try:
         Mentor2Course.objects.get(user = request.user.mentor,course=course)
    except:
        u2c = Mentor2Course.objects.create(
            user = request.user.mentor,
            course = course
        )
    messages.info(request, _('You was joined to this course.'))
    return redirect('mentor-cabinet')
