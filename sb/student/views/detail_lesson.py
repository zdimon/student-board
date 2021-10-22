from django.shortcuts import render
from course.models import Course, Lesson, Topic, Lab
from django.contrib import messages
from student.models import Student2Course
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect



def detail_lesson(request, lesson_id):
    if not request.user.is_authenticated:
        return redirect('user-login')
    
    lesson = Lesson.objects.get(pk=lesson_id)
    if not Course.is_paid(request.user.student,lesson.course):
        messages.info(request, 'Для просмотра необходимо оплатить курс.')
        return redirect('prepay', course_id=lesson.course.pk)

    topics = Topic.objects.filter(lesson=lesson)
    try:
        lab = Lab.objects.get(lesson=lesson)
    except:
        lab = None
    return render(request,'student/detail_lesson.html', {"lesson": lesson, "topics": topics, "lab": lab})
