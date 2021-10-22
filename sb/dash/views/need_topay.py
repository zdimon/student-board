from django.shortcuts import render
from course.models import Course

def need_topay(request,course_id):
    course = Course.objects.get(pk=course_id)
    return render(request,'need_topay.html', {"course": course})  
