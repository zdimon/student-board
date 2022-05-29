from xml import dom
from django.shortcuts import render
from django.contrib.auth import login
from django.shortcuts import redirect
from mentor.models import Invitation
from mentor.forms.invite import InviteForm
from django.contrib import messages
from student.models import EmailTemplate
from django.core.mail import send_mail
from sb.settings import EMAIL_ADMIN, DOMAIN
from django.template.loader import render_to_string
from django.template import Template, Context
from django.utils.html import strip_tags
from django.core.mail import send_mail


def invite(request):
    form = InviteForm()
    if request.method == 'POST':
        form = InviteForm(request.POST)
        if form.is_valid():
            messages.add_message(request, messages.INFO, 'A letter has been created!')
            invitation = form.save()
            tpl =  EmailTemplate.objects.get(alias='invitation')
            title = tpl.title
            url = '%s/%s/%s' % (DOMAIN,'student/invite',invitation.uuid)
            link = '%s' % url
            content = tpl.content
            t = Template(content)
            cmname = '%s (%s)' % (invitation.course.name, invitation.group.name)
            c = Context({"name": invitation.name, 
                         "coursename": cmname,
                         "sitename": DOMAIN,
                         "link": link})
            content = t.render(c)
            plain_message = strip_tags(content)
            send_mail(
                title,
                plain_message,
                EMAIL_ADMIN,
                [invitation.email],
                fail_silently=False,
                html_message=content
            )
    return render(request,'mentor/invite.html',{"form": form})
