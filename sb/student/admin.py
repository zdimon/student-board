from django.contrib import admin
from .models import Student, StudentGroup, Student2Course, Student2Lab, StudentPayment

# Register your models here.


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['username', 'fname', 'lname', 'group']

@admin.register(StudentGroup)
class StudentGroupAdmin(admin.ModelAdmin):
    pass


@admin.register(Student2Course)
class Student2CourseGroupAdmin(admin.ModelAdmin):
    pass

@admin.register(Student2Lab)
class Student2LabAdmin(admin.ModelAdmin):
    list_display = ['lab', 'user', 'file', 'gitlink']

@admin.register(StudentPayment)
class StudentPaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'course','fname','lname','cost','mark', 'type', 'is_done']