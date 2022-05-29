from django.shortcuts import render
from mentor.models import Invitation
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse
from student.models import Student
import random
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.utils.translation import ugettext as _


def invite(request, uuid):
    invitation = Invitation.objects.get(uuid=uuid)
    try:
        user = User.objects.get(username=invitation.email)
        login(request, user)
        if not user.student.lname:
            mes = user.student.fname+', '+_(' заполните пожалуйста свой профиль.')
            messages.add_message(request, messages.INFO, mes)
            return redirect(reverse('student-profile'))
        return redirect(reverse('student-cabinet'))
    except Exception as e:
        # print(e)
        paswd = random.randint(1111,9999)
        student = Student()
        student.group = invitation.group
        student.username = invitation.email
        student.is_active = True
        student.fname = invitation.name
        student.email = invitation.email
        student.set_password(paswd)
        try:
            student.save()
            login(request, student)
        except:
            messages.add_message(request, messages.ERROR, _('Произошла ошибка!'))
        
    return render(request,'student/invite.html', {'paswd': paswd})
