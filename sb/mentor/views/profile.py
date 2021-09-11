from django.shortcuts import render
from django.contrib.auth import login
from django.shortcuts import redirect
from mentor.models import Mentor


def profile(request):
   
    return render(request,'mentor/profile.html')
