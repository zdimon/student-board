from django.shortcuts import render
from course.models import Lab
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from student.forms.lab import Student2LabForm
from student.models import Student2Lab, Exam, Student2ExamQuestion, Student2ExamAnswer
from student.forms.exam_pass import Student2ExamAnswerForm

def exam_pass(request, exam_id):
    if not request.user.is_authenticated:
        return redirect('user-login')
    exam = Exam.objects.get(pk=exam_id)
    try:
        obj = Student2ExamAnswer.objects.get(user=request.user.student, exam=exam)
    except:
        obj = None
    form = Student2ExamAnswerForm(instance=obj)
    if request.method == 'POST':
        form = Student2ExamAnswerForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.info(request, _('Thank you. Your work has saved and sended to the mentor.'))
        else:
            messages.info(request, _('Error.'))
            print(form.errors)
    questions = Student2ExamQuestion.objects.filter(user=request.user.student, exam=exam)
    return render(request,'student/exam_pass.html', {"exam": exam, "questions": questions, "form": form, "obj": obj})
