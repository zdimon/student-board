from django.shortcuts import render
from course.models import Lab
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from student.forms.lab import Student2LabForm

def detail_lab(request, lab_id):
    lab = Lab.objects.get(pk=lab_id)
    form = Student2LabForm()
    return render(request,'student/detail_lab.html', {"lab": lab, "form": form})
