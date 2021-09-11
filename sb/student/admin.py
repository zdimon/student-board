from django.contrib import admin
from .models import Student, StudentGroup, Student2Course

# Register your models here.


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass

@admin.register(StudentGroup)
class StudentGroupAdmin(admin.ModelAdmin):
    pass


@admin.register(Student2Course)
class Student2CourseGroupAdmin(admin.ModelAdmin):
    pass