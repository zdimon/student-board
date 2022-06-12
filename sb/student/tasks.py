from student.models import EmailTemplate
from django.core.mail import send_mail
from django.template import Template, Context
from sb.settings import EMAIL_ADMIN, DOMAIN
from django.utils.html import strip_tags


def pay_course_notification(course, user):
    tpl = EmailTemplate.objects.get(alias='pay-course')
    title = tpl.title
    url = '%s/%s/%s/%s' % (DOMAIN,'student/paidcourse',user.uuid,course.pk)
    link = '<a href="%s">%s</a>' % (url,url)
    content = tpl.content
    t = Template(content)
    c = Context({"course_name": course.name, 
                    "title": tpl.title,
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


def pay_lesson_notification(lesson, user):
    tpl = EmailTemplate.objects.get(alias='pay-lesson')
    title = tpl.title
    url = '%s/%s/%s/%s' % (DOMAIN,'student/paidlesson',user.uuid,lesson.pk)
    link = '<a href="%s">%s</a>' % (url,url)
    content = tpl.content
    t = Template(content)
    c = Context({"lesson_name": lesson.title, 
                "course_name": lesson.course.name,
                    "title": tpl.title,
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