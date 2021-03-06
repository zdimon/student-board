from curses.ascii import EM
from django.core.management.base import BaseCommand
from student.models import EmailTemplate


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Start loading email templates')
        EmailTemplate.objects.all().delete()
        title = 'Приглашение на курсы'
        content = '''
            Зравствуте {{ name }}.
            Ваc сприветствует сайт {{ sitename }} и его автор Жариков Дмитрий.
            Вы получили приглашение пройти курс {{ coursename }}.
            Для того, чтобы воспользоваться приглашением, пройдите по ссылке ниже.
            {{ link }}
        '''
        tpl = EmailTemplate()
        tpl.alias = 'invitation'
        tpl.title = title
        tpl.content = content
        tpl.save()

        title = 'Уведомление о новом уроке!'
        content = '''
            Зравствуте {{ name }}.
            Ваc сприветствует сайт {{ sitename }} и его автор Жариков Дмитрий.
            На сайте опубликован новый урок "{{ title }}".
            Для того, чтобы ознакомиться нажмите ссылку ниже.
            {{ link }}
        '''
        tpl = EmailTemplate()
        tpl.alias = 'lesson-notification'
        tpl.title = title
        tpl.content = content
        tpl.save()

        title = 'Оплата курса'
        content = '''
            Зравствуте {{ name }}.
            Вы успешно оплатили курс "{{ course_name }}".
            Для того, чтобы ознакомиться с курсом нажмите ссылку ниже.
            {{ link }}
        '''
        tpl = EmailTemplate()
        tpl.alias = 'pay-course'
        tpl.title = title
        tpl.content = content
        tpl.save()

        title = 'Оплата урока'
        content = '''
            Зравствуте {{ name }}.
            Вы успешно оплатили урок "{{ lesson_name }}" курса "{{ course_name }}".
            Для того, чтобы ознакомиться с уроком нажмите ссылку ниже.
            {{ link }}
        '''
        tpl = EmailTemplate()
        tpl.alias = 'pay-lesson'
        tpl.title = title
        tpl.content = content
        tpl.save()