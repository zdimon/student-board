from django.shortcuts import render
from course.models import Lab, Kursak
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from student.forms.lab import Student2LabForm
from student.models import Student2Lab


def detail_kursak(request, kursak_id):
    kursak = Kursak.objects.get(pk=kursak_id)
    return render(request,'student/detail_kursak.html', {"kursak": kursak})
