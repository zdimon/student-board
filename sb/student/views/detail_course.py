from django.shortcuts import render
from course.models import Course, Lesson
from django.contrib import messages
from student.models import Student2Course
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from django.utils.translation import get_language

def detail_course(request, course_name_slug):
    
    course_lang_arr = course_name_slug.split('-')
    course_lang = course_lang_arr[len(course_lang_arr)-1]
    print(course_lang)
    course = Course.objects.get(name_slug=course_name_slug)
    lessons = Lesson.objects.filter(course=course).order_by('number')
    return render(request,'student/detail_course.html', {"course": course, "lessons": lessons})
