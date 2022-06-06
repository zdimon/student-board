from django.shortcuts import render
from course.models import Course
from student.models import Student2Course


def courses(request):
    courses = Course.objects.all()
    for course in courses:
        course.is_paid = Course.is_course_paid(request.user.student, course)
    joined_courses = []
    if request.user.is_authenticated:
        for c in Student2Course.objects.filter(user=request.user.student):
            joined_courses.append(c.course.pk)
    return render(request, 'dash/courses.html', {"courses": courses,"joined_courses": joined_courses})
