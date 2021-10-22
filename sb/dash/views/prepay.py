from django.shortcuts import render
from course.models import Course
from student.models import Student2Course, StudentPayment, StudentGroup
from django.shortcuts import redirect


def prepay(request,course_id):
    groups = StudentGroup.objects.all().order_by('name')
    course = Course.objects.get(pk=course_id)
    if request.method == "POST":
        p = StudentPayment()
        p.mark = request.POST.get("mark",'')
        p.course = course
        if p.mark == '3':
            p.cost = 1300
        if p.mark == '4':
            p.cost = 1400
        if p.mark == '5':
            p.cost = 1500        
        if request.user.is_authenticated:
            
            p.user = request.user.student
            p.course = course
            p.fname = request.user.student.fname
            p.lname = request.user.student.lname
            p.sname = request.user.student.surname  


        else:
            p.fname = request.POST.get("first_name",'')
            p.lname = request.POST.get("last_name",'')
            p.sname = request.POST.get("surname",'') 
            p.email = request.POST.get("email",'') 

        p.save()
        return redirect('buy-course', order_id=p.id)
        
    
    return render(request, 'dash/prepay.html', {"groups": groups})
