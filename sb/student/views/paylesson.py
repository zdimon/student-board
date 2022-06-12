from django.shortcuts import render
from mentor.models import Invitation
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse
from student.models import Student, LessonPayment
from course.models import Lesson
from django.contrib import messages
from django.utils.translation import ugettext as _
from student.tasks import pay_lesson_notification


def paylesson(request, lesson_id):
    lesson = Lesson.objects.get(pk=lesson_id)
    if request.user.student.account > 49:
        lp = LessonPayment()
        lp.user = request.user.student
        lp.lesson = lesson
        lp.save()
        request.user.student.account = request.user.student.account - 50
        request.user.student.save()
        messages.add_message(request, messages.INFO, _('Вы успешно оплатили урок'))
        pay_lesson_notification(lesson, request.user.student)
    else:
        messages.add_message(request, messages.INFO, _('У вас недостаточно средств на счету'))
    return redirect(reverse('detail-lesson-student', kwargs={"lesson_id": lesson_id}))
    