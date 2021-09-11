from django.shortcuts import render


def cabinet(request):
    return render(request, 'dash/cabinet.html', {})
