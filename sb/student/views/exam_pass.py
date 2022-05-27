from django.shortcuts import render
from course.models import Lab
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from student.forms.lab import Student2LabForm
from student.models import Student2Lab, Exam, Student2ExamQuestion, Student2ExamAnswer, ExamQuestion
from student.forms.exam_pass import Student2ExamAnswerForm
import random

def bilet_gen(exam,student):
    questions = []
    for q in ExamQuestion.objects.filter(exam=exam):
        questions.append(q.id)
    random.shuffle(questions)
    question1 = ExamQuestion.objects.get(pk=questions[0])
    question2 = ExamQuestion.objects.get(pk=questions[1])
    question3 = ExamQuestion.objects.get(pk=questions[2])
    s2q1 = Student2ExamQuestion()
    s2q1.user = student
    s2q1.question = question1
    s2q1.exam = exam
    s2q1.save()

    s2q1 = Student2ExamQuestion()
    s2q1.user = student
    s2q1.question = question2
    s2q1.exam = exam
    s2q1.save()

    s2q1 = Student2ExamQuestion()
    s2q1.user = student
    s2q1.question = question3
    s2q1.exam = exam
    s2q1.save()

def exam_pass(request, exam_id):
    if not request.user.is_authenticated:
        return redirect('user-login')
    student = request.user.student
    exam = Exam.objects.get(pk=exam_id)
    try:
        obj = Student2ExamAnswer.objects.get(user=request.user.student, exam=exam)
    except:
        bilet_gen(exam,student)
        obj = Student2ExamAnswer.objects.create(user=student, exam=exam)

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
