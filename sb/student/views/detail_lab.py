from django.shortcuts import render
from course.models import Lab
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from student.forms.lab import Student2LabForm
from student.models import Student2Lab


def detail_lab(request, lab_id):
    if not request.user.is_authenticated:
        return redirect('user-login')
    lab = Lab.objects.get(pk=lab_id)
    try:
        exists = Student2Lab.objects.get(user=request.user.student, lab=lab)
        is_done = True
    except Exception as e:
        is_done = False
    s2l = Student2Lab()
    s2l.user = request.user.student
    s2l.lab = lab
    form = Student2LabForm(instance=s2l)
    if request.method == 'POST':
        form = Student2LabForm(request.POST, request.FILES, instance=s2l)
        if form.is_valid():
            try:
                exists = Student2Lab.objects.get(user=request.user.student, lab=lab)
                messages.warning(request, _('You already sent this lab!'))
            except Exception as e:
                form.save()
                messages.info(request, _('Thank you. Your work has saved and sended to the mentor.'))
                is_done = True
    return render(request,'student/detail_lab.html', {"lab": lab, "form": form, "is_done": is_done})
