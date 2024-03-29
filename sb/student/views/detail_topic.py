from django.shortcuts import render
from course.models import Course, Lesson, Topic, Lab
from django.contrib import messages
from student.models import Student2Course
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect



def detail_topic(request, lesson, topic):
    key = lesson+'--'+topic
    topic = Topic.objects.filter(alias=key).first()
    layout = 'layout.html'
    return render(request,'student/detail_topic.html', {"topic": topic, "layout": layout})

def detail_topic_empty(request, lesson, topic):
    key = lesson+'--'+topic
    topic = Topic.objects.filter(alias=key).first()
    layout = 'layout_empty.html'
    return render(request,'student/detail_topic.html', {"topic": topic, "layout": layout})
