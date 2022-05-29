from django.shortcuts import render
from django.contrib.auth import login
from django.shortcuts import redirect
from mentor.models import Mentor, Mentor2Course, Mentor2Group
from course.models import Course

def groups(request):
    groups = Mentor2Group.objects.filter(user=request.user.mentor)
    return render(request,'mentor/groups.html',{"groups": groups})
