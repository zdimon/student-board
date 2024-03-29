from django.shortcuts import render
from course.models import Course, Lesson, Topic, Lab
from django.contrib import messages
from student.models import Student2Course
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect



def detail_lesson(request, lesson):
    #if not request.user.is_authenticated:
    #    return redirect('user-login')
    
    lesson = Lesson.objects.get(name_slug=lesson)
    if not Course.is_paid(request.user,lesson):
        messages.info(request, 'Для просмотра урока необходима оплата.')
        return redirect('prepay', course_id=lesson.course.pk, lesson_id=lesson_id)

    topics = Topic.objects.filter(lesson=lesson)
    try:
        lab = Lab.objects.get(lesson=lesson)
    except:
        lab = None
    return render(request,'student/detail_lesson.html', {"lesson": lesson, "topics": topics, "lab": lab})
