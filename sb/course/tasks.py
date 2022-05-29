from sb.celery import app
from course.models import NewsLetter, Subscription
from django.core.mail import send_mail

@app.task
def send_letters_task(letter_id):
    
    letter = NewsLetter.objects.get(pk=letter_id)
    users = []
    for s in Subscription.objects.filter(is_subscribed=True):
        send_mail(
            letter.title,
            letter.txt_content,
            'zdimon@pressa.ru',
            [s.email],
            html_message=letter.content,
            fail_silently=False,
        )
        print('Send letter for %s' % s.email)