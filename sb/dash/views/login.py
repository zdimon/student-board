from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import login as l


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                l(request, user)   
        else:
            print('Error data!')     

    return render(request, 'dash/welcome.html', {})
