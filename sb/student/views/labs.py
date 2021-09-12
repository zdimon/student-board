from django.shortcuts import render
from course.models import Course
from django.contrib import messages
from student.models import Student2Course, Student2Lab
from course.models import Lab
from django.shortcuts import redirect


def labs(request,course_id='all'):
    courses = []
    if course_id=='all':
        tmp = Student2Course.objects.filter(user=request.user.student)
        for c in tmp:
            courses.append(c.course)
    else:
        courses.append(Course.objects.get(pk=course_id))

    exist_labs = []
    for s2l in Student2Lab.objects.filter(user=request.user.student):
        exist_labs.append(s2l.lab.pk)
    return render(request,'student/labs.html', {"courses": courses, "exist_labs": exist_labs})


def delete_lab(request,lab_id):
    lab = Lab.objects.get(pk=lab_id)
    try:
        s2l = Student2Lab.objects.get(user=request.user.student, lab=lab)
        s2l.delete()
        messages.warning(request, _('Your report was deleted.'))
    except:
        pass
    return redirect('student-labs')