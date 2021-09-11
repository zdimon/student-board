from django.shortcuts import render
from django.contrib.auth import login
from django.shortcuts import redirect
from mentor.models import Mentor


def cabinet(request):
    return render(request,'mentor/cabinet.html')
