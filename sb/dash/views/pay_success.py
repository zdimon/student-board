from django.shortcuts import render


def pay_success(request):
   
    return render(request, 'dash/pay_success.html')
