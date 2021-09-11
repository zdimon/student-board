from django.shortcuts import render
from course.models import Course
from student.models import Student2Course


def courses(request):
    courses = Course.objects.all()
    joined_courses = []
    for c in Student2Course.objects.filter(user=request.user.student):
        joined_courses.append(c.course.pk)
    return render(request, 'dash/courses.html', {"courses": courses,"joined_courses": joined_courses})