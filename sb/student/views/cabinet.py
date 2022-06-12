from django.shortcuts import render
from course.models import Course
from django.contrib import messages
from student.models import Student2Course, Exam, CoursePayment

def cabinet(request):
    pc = CoursePayment.objects.filter(user=request.user.student)
    courses = []
    for it in pc:
        courses.append(it.course)
    for course in courses:
        course.is_paid = Course.is_course_paid(request.user.student, course)
    exams = Exam.objects.filter(group=request.user.student.group)
    joined_courses = []
    for c in Student2Course.objects.filter(user=request.user.student):
        joined_courses.append(c.course.pk)
    return render(request,'student/cabinet.html', {"courses": courses, "joined_courses": joined_courses, "exams": exams})
