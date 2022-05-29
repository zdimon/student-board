from xml import dom
from django.shortcuts import render
from django.contrib.auth import login
from django.shortcuts import redirect
from course.models import Lesson
from student.models import StudentGroup2Course, Student, EmailTemplate
from sb.settings import EMAIL_ADMIN, DOMAIN
from django.template.loader import render_to_string
from django.template import Template, Context
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.contrib import messages

def send_notification(user,lesson):
    tpl = EmailTemplate.objects.get(alias="lesson-notification")
    print(user)
    title = tpl.title
    url = '%s/%s/%s/%s' % (DOMAIN,'student/newlesson',user.uuid,lesson.pk)
    link = '<a href="%s">%s</a>' % (url,url)
    content = tpl.content
    t = Template(content)
    c = Context({"name": user.fname, 
                    "title": lesson.title,
                    "link": link})
    content = t.render(c)
    plain_message = strip_tags(content)
    send_mail(
        title,
        plain_message,
        EMAIL_ADMIN,
        [user.email],
        fail_silently=False,
        html_message=content
    )

def notify(request, lesson_id):
    lesson = Lesson.objects.get(pk=lesson_id)
    groups = StudentGroup2Course.objects.filter(course=lesson.course)
    students = []
    if request.method == 'POST':
        users = request.POST.getlist('student[]')
        for user in users:
            student = Student.objects.get(pk=user) 
            send_notification(student,lesson)
        messages.add_message(request, messages.INFO, 'A letter has been created!')
    for group in groups:
        for student in group.group.student_set.all():
            students.append(student)
    return render(request,'mentor/notify.html',{"lesson": lesson, "students": students})
