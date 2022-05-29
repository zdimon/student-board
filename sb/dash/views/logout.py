from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import logout as lout
from django.shortcuts import redirect


def logout(request):
    lout(request)
    return redirect('/')
