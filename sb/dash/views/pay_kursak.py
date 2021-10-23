from django.shortcuts import render
from course.models import Course, Kursak
from student.models import Student2Course, StudentPayment, StudentGroup
from django.shortcuts import redirect
from student.models import Student
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import login


def pay_kursak(request,kursak_id):
    groups = StudentGroup.objects.all().order_by('name')
    kursak = Kursak.objects.get(pk=kursak_id)


    if request.method == "POST":
        p = StudentPayment()
        p.kursak = kursak
        p.type="kursak"
        p.cost = 1000  
        p.mark = request.POST.get("mark",'')      
        if request.user.is_authenticated:
            
            p.user = request.user.student
            p.fname = request.user.student.fname
            p.lname = request.user.student.lname
            p.sname = request.user.student.surname  


        else:
            p.fname = request.POST.get("first_name",'')
            p.lname = request.POST.get("last_name",'')
            p.sname = request.POST.get("surname",'') 
            p.email = request.POST.get("email",'') 
            group = StudentGroup.objects.get(pk=request.POST.get("group",''))
            s = Student()
            s.fname = request.POST.get("first_name",'')
            s.lname = request.POST.get("last_name",'')
            s.username = request.POST.get("email",'')
            s.surname = request.POST.get("surname",'') 
            s.group = group
            s.account = 0
            s.set_password(request.POST.get("password",''))
            s.email = request.POST.get("email",'') 
            s.is_active = True
            s.save()
            messages.info(request, _('Вы были зарегистрированы на сайте с указанным логином и паролем.'))
            p.user = s
            login(request, s)
        p.save()
        return redirect('buy-course', order_id=p.id)
        
    
    return render(request, 'dash/pay_kursak.html', {"groups": groups, "kursak": kursak})
