from django.contrib import admin
from .models import Student, StudentGroup

# Register your models here.


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass

@admin.register(StudentGroup)
class StudentGroupAdmin(admin.ModelAdmin):
    pass